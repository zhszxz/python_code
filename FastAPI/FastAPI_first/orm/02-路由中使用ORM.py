from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 1. 创建异步引擎
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:739627@106.54.2.137:3306/FastAPI_first?charset=utf8mb4"
)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)


# 2. 定义 ORM 基类
class Base(DeclarativeBase):
    __abstract__ = True

    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        comment="创建时间"
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )


# 3. 定义 Book 表
class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="书籍ID"
    )

    bookname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="书名"
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="作者"
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="价格"
    )

    publisher: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="出版社"
    )


# 4. 创建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 5. FastAPI 启动时建表
# @app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 需求：查询功能的接口，查询图书 → 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)


# 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@app.get("/books")
async def get_books(session=Depends(get_database)):
    """
    查询所有图书
    """
    books = await session.execute(select(Book))
    return books.scalars().all()
