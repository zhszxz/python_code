"""
sqlalchemy 删除操作
"""

from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 创建异步引擎
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:739627@106.54.2.137:3306/FastAPI_first?charset=utf8mb4"
)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)


# 定义 ORM 基类
class Base(DeclarativeBase):
    __abstract__ = True

    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        server_default=func.now(),
        comment="创建时间"
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )


# 定义 Book 表
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
        yield session


# 1.orm删除
@app.delete("/book/{book_id}")
async def delete_book(
        book_id: int,
        db: AsyncSession = Depends(get_database)
):
    book = await db.get(Book, book_id)

    if not book:
        return {"message": "书籍不存在"}

    await db.delete(book)

    await db.commit()

    return {"message": "删除成功"}


# 2.手动delete
@app.delete("/book/{book_id}")
async def delete_book(
        book_id: int,
        db: AsyncSession = Depends(get_database)
):
    await db.execute(
        delete(Book).where(Book.id == book_id)
    )

    await db.commit()

    return {"message": "删除成功"}
