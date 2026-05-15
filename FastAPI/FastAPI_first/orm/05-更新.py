"""
sqlalchemy 更新操作
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import DateTime, func, String, Float, update
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


# 定义更新数据模型
class BookUpdate(BaseModel):
    bookname: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    publisher: Optional[str] = None


async def get_database():
    async with AsyncSessionLocal() as session:
        yield session


# 1.orm更新
@app.put("/book/{book_id}")
async def update_orm(
        book_id: int,
        book_data: BookUpdate,
        db: AsyncSession = Depends(get_database)
):
    # 1.orm更新必须先拿到对象
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 2.提取非空元素为字典
    update_data = book_data.model_dump(exclude_unset=True)

    # 3.动态修改对象属性
    for k, v in update_data.items():
        setattr(book, k, v)

    # 4.自动检测变化属性,然后生成sql
    await db.commit()
    await db.refresh(book)
    return book


# 2.手动update
@app.put("/update/{book_id}")
async def update_book(
        book_id: int,
        db: AsyncSession = Depends(get_database)
):
    await db.execute(
        update(Book)
        .where(Book.id == book_id)
        .values(bookname='三国演义', publisher='大明出版社')
    )

    await db.commit()
    return await db.get(Book, book_id)


# 3.批量更新
@app.put("/batch")
async def update_batch(db: AsyncSession = Depends(get_database)):
    result = await db.execute(update(Book).where(Book.price > 100).values(price=Book.price * 0.9))
    await db.commit()
    return {'update': result.rowcount}
