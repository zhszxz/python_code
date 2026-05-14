from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, func, String, Float  # SQLAlchemy数据类型和函数
from sqlalchemy.ext.asyncio import create_async_engine  # 异步数据库引擎创建器
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # ORM基类和映射工具

app = FastAPI()

# ============================================
# 1. 配置并创建异步数据库引擎
# ============================================
# 异步MySQL数据库连接URL
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:739627@106.54.2.137:3306/FastAPI_first?charset=utf8mb4"
)

# 创建异步引擎实例
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 开启SQL日志输出，便于调试
    pool_size=10,  # 连接池大小：保持10个长期连接
    max_overflow=20  # 最大溢出连接数：超出pool_size后最多再创建20个临时连接
)


# ============================================
# 2. 定义ORM基类（所有模型表的父类）
# ============================================
class Base(DeclarativeBase):
    """
    ORM基类，提供所有表共有的字段和方法
    __abstract__ = True 表示这是一个抽象基类，不会单独创建表
    """
    __abstract__ = True

    create_time: Mapped[datetime] = mapped_column(
        DateTime,  # 数据库字段类型：DATETIME
        insert_default=func.now(),  # 插入时使用当前时间作为默认值
        default=func.now(),  # Python层面的默认值
        comment="创建时间"  # 字段注释
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime,  # 数据库字段类型：DATETIME
        insert_default=func.now(),  # 插入时使用当前时间
        default=func.now(),  # Python层面的默认值
        onupdate=func.now(),  # 每次更新记录时自动更新为当前时间
        comment="更新时间"  # 字段注释
    )


# ============================================
# 3. 定义Book书籍表模型
# ============================================
class Book(Base):
    """
    书籍信息表模型
    继承自Base类，自动包含create_time和update_time字段
    """
    __tablename__ = "book"  # 指定数据库中的表名为"book"

    # 主键ID：唯一标识每本书
    id: Mapped[int] = mapped_column(
        primary_key=True,  # 设为主键
        autoincrement=True,  # 启用自增
        comment="书籍ID"  # 字段注释
    )

    # 书名字段：存储书籍名称
    bookname: Mapped[str] = mapped_column(
        String(255),  # 字符串类型，最大长度255字符
        nullable=False,  # 不允许为空
        comment="书名"  # 字段注释
    )

    # 作者字段：存储书籍作者
    author: Mapped[str] = mapped_column(
        String(255),  # 字符串类型，最大长度255字符
        nullable=False,  # 不允许为空
        comment="作者"  # 字段注释
    )

    # 价格字段：存储书籍价格
    price: Mapped[float] = mapped_column(
        Float,  # 浮点数类型
        nullable=False,  # 不允许为空
        comment="价格"  # 字段注释
    )

    # 出版社字段：存储出版机构名称
    publisher: Mapped[str] = mapped_column(
        String(255),  # 字符串类型，最大长度255字符
        nullable=False,  # 不允许为空
        comment="出版社"  # 字段注释
    )


# ============================================
# 4. 定义创建表的异步函数
# ============================================
async def create_tables():
    """
    异步创建所有继承自Base的表
    如果表已存在则不会重复创建
    """
    # 使用异步上下文管理器获取数据库连接
    async with async_engine.begin() as conn:
        # run_sync用于在异步环境中执行同步方法
        # Base.metadata.create_all会检查并创建所有未存在的表
        await conn.run_sync(Base.metadata.create_all)


# ============================================
# 5. 注册FastAPI启动事件：应用启动时自动建表
# ============================================
@app.on_event("startup")
async def startup_event():
    """
    FastAPI应用启动时执行的初始化操作
    在这里调用create_tables确保数据库表结构已就绪
    """
    await create_tables()


# ============================================
# 6. 定义根路由（测试接口）
# ============================================
@app.get("/")
async def root():
    """
    根路径GET请求处理函数
    用于验证服务是否正常启动
    """
    return {"message": "Hello World"}
