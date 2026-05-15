"""
sqlalchemy 查询操作
"""
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import DateTime, func, String, Float, select, or_
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


# 1.查询全部数据
@app.get("/books")
async def get_books(
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


# 2.主键查询
@app.get("/book/{book_id}")
async def get_book(
        book_id: int,
        db: AsyncSession = Depends(get_database)
):
    book = await db.get(Book, book_id)
    return book


# 3.where条件查询
@app.get("/books/price")
async def get_books_by_price(
        price: float,
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.price > price))
    return result.scalars().all()


# 4.异常返回
@app.get("/exception/{book_id}")
async def get_book(
        book_id: int,
        db: AsyncSession = Depends(get_database)
):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# 5.模糊查询
@app.get("/like")
async def search_book(
        keyword: str,
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.bookname.like(f"%{keyword}%")))
    return result.scalars().all()


# 6.排序
@app.get("/order")
async def order_book(
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).order_by(Book.price.desc()))
    return result.scalars().all()


# 7.分页
@app.get("/books/page")
async def get_books_page(
        page: int = 1,
        size: int = 10,
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).offset((page - 1) * size).limit(size))
    return result.scalars().all()


# 8.AND条件
@app.get("/books/and")
async def get_books_and(
        book_name: str,
        author: str,
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.bookname == book_name, Book.author == author))
    return result.scalars().all()


# 9.OR条件
@app.get("/books/or")
async def get_books_or(book_name: str,
                       author: str,
                       db: AsyncSession = Depends(get_database)
                       ):
    result = await db.execute(select(Book).where(or_(
        Book.bookname == book_name,
        Book.author == author
    )))
    return result.scalars().all()


# 10.in查询
@app.get("/books/in")
async def get_books_in(book_ids: list[int] = Query(),
                       db: AsyncSession = Depends(get_database)
                       ):
    result = await db.execute(select(Book).where(Book.id.in_(book_ids)))
    return result.scalars().all()


# 11.between查询
@app.get("/books/between")
async def get_books_between(
        min_price: float,
        max_price: float,
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.price.between(min_price, max_price)))
    return result.scalars().all()


# 12.count计数
@app.get("/books/count")
async def get_books_count(
        db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(func.count()).select_from(Book))
    return result.scalar()
