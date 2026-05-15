"""
sqlalchemy 新增操作
"""

from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import DateTime, func, String, Float
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


# 定义新增数据模型
class BookCreate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str


async def get_database():
    async with AsyncSessionLocal() as session:
        yield session


# 1.新增图书
@app.post("/book")
async def create_book(
        book: BookCreate,
        db: AsyncSession = Depends(get_database)):
    # new_book = Book(
    #     bookname=book.bookname,
    #     author=book.author,
    #     price=book.price,
    #     publisher=book.publisher
    # )

    # 推荐写法: 将 book 转为 dict, 再解包为关键字参数
    new_book = Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)  # 数据库自动生成字段回填
    return 'success'


# 2.批量新增
@app.post("/book/batch")
async def create_batch(db: AsyncSession = Depends(get_database)):
    books = [
        Book(
            bookname="Python",
            author="Tom",
            price=99,
            publisher="A"
        ),
        Book(
            bookname="FastAPI",
            author="Jack",
            price=88,
            publisher="B"
        )
    ]
    db.add_all(books)
    await db.commit()
    return 'success'
