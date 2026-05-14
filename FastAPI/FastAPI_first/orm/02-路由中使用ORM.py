from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select  # SQLAlchemy数据类型、函数和查询方法
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession  # 异步引擎、会话工厂和会话类
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # ORM基类和映射工具

app = FastAPI()

# ============================================
# 1. 配置并创建异步数据库引擎
# ============================================
ASYNC_DATABASE_URL = (
    "mysql+aiomysql://root:739627@106.54.2.137:3306/FastAPI_first?charset=utf8mb4"
)

# 创建异步引擎实例
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,           # 开启SQL日志输出，便于调试查看生成的SQL语句
    pool_size=10,        # 连接池大小：保持10个长期连接
    max_overflow=20      # 最大溢出连接数：超出pool_size后最多再创建20个临时连接
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

    # 创建时间字段：记录数据首次插入的时间
    create_time: Mapped[datetime] = mapped_column(
        DateTime,                    # 数据库字段类型：DATETIME
        insert_default=func.now(),   # 插入时使用当前时间作为默认值
        default=func.now(),          # Python层面的默认值
        comment="创建时间"            # 字段注释
    )

    # 更新时间字段：记录数据最后更新的时间
    update_time: Mapped[datetime] = mapped_column(
        DateTime,                    # 数据库字段类型：DATETIME
        insert_default=func.now(),   # 插入时使用当前时间
        default=func.now(),          # Python层面的默认值
        onupdate=func.now(),         # 每次更新记录时自动更新为当前时间
        comment="更新时间"            # 字段注释
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
        primary_key=True,       # 设为主键
        autoincrement=True,     # 启用自增
        comment="书籍ID"         # 字段注释
    )

    # 书名字段：存储书籍名称
    bookname: Mapped[str] = mapped_column(
        String(255),            # 字符串类型，最大长度255字符
        nullable=False,         # 不允许为空
        comment="书名"           # 字段注释
    )

    # 作者字段：存储书籍作者
    author: Mapped[str] = mapped_column(
        String(255),            # 字符串类型，最大长度255字符
        nullable=False,         # 不允许为空
        comment="作者"           # 字段注释
    )

    # 价格字段：存储书籍价格
    price: Mapped[float] = mapped_column(
        Float,                  # 浮点数类型
        nullable=False,         # 不允许为空
        comment="价格"           # 字段注释
    )

    # 出版社字段：存储出版机构名称
    publisher: Mapped[str] = mapped_column(
        String(255),            # 字符串类型，最大长度255字符
        nullable=False,         # 不允许为空
        comment="出版社"         # 字段注释
    )

# ============================================
# 4. 定义根路由（测试接口）
# ============================================
@app.get("/")
async def root():
    """
    根路径GET请求处理函数
    用于验证服务是否正常启动
    """
    return {"message": "Hello World"}


# ============================================
# 5. 配置数据库会话工厂（用于依赖注入）
# ============================================

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,              # 绑定之前创建的数据库引擎
    class_=AsyncSession,            # 指定使用异步会话类
    expire_on_commit=False          # 提交后会话不过期，避免重新查询数据库，提高性能
)


# ============================================
# 6. 定义数据库会话依赖项
# ============================================
async def get_database():
    """
    数据库会话依赖项生成器
    负责创建、管理和关闭数据库会话，确保资源正确释放
    使用yield实现依赖注入，支持事务的自动提交或回滚
    """
    # 创建新的异步会话实例
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 将会话提供给路由函数使用
            await session.commit()  # 如果路由函数执行成功，提交事务
        except Exception:
            await session.rollback()  # 如果发生异常，回滚事务
            raise  # 重新抛出异常，让上层处理
        finally:
            await session.close()  # 无论成功或失败，最终都会关闭会话，释放资源


# ============================================
# 7. 定义查询所有图书的API接口
# ============================================
@app.get("/books")
async def get_books(session=Depends(get_database)):
    """
    查询所有图书记录的API接口
    
    参数:
        session: 通过Depends注入的数据库会话对象，由get_database依赖项提供
    
    返回:
        包含所有书籍信息的列表
    """
    # 执行SELECT查询：select(Book)等价于SELECT * FROM book
    books = await session.execute(select(Book))
    
    # scalars()提取标量值（即Book对象），all()获取所有结果
    # 返回的是Book模型实例列表，FastAPI会自动序列化为JSON
    return books.scalars().all()
