"""
sqlalchemy 查询操作
"""
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

# 2. 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)


# 3. 定义 ORM 基类
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


# 4. 定义 Book 表
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
async def get_books(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
    return result.scalars().all()
    # return result.scalars().first()
    # return await db.get(Book, 1)


@app.get("/book/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


@app.get("/search/{price}")
async def search_book(price: float, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= price))
    return result.scalars().all()
