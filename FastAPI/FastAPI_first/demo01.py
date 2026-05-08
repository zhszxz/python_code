from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

# ==================== FastAPI 请求路由与请求参数的获取 ====================
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 需求：访问 /user/hello 返回 {"message": "我正在学习FastAPI......"}
@app.get("/user/hello")
async def user_hello():
    return {"message": "我正在学习FastAPI......"}


# 获取路径参数
# @app.get("/book/{id}")
async def get_book(id: int):
    return {"id": id, "message": f"这是第{id}本书"}


# Path的理解：借用参数默认值的位置，存放参数的描述信息，如是否必须、默认值、范围等
@app.get("/book/{id}")
async def get_book(id: int = Path(..., ge=0, lt=101)):
    return {"id": id, "message": f"这是第{id}本书"}


# 参数校验: name 长度必须在 2 到 10 之间
@app.get("/author/{name}")
async def author(name: str = Path(..., min_length=2, max_length=10)):
    return {"name": name, "message": f"作者名字是{name}"}


# 获取Query参数，函数参数默认会被当作Query参数
# Query的理解：同Path，只是描述的是查询参数
@app.get("/news/list")
async def news_list(skip: int = Query(0, description="跳过的记录数", ge=0, le=100),
                    limit: int = Query(..., le=50)):
    return {"skip": f"跳过前{skip}条记录", "limit": f"返回{limit}条记录"}


# 获取请求体参数
# Field的理解：同Path和Query，只是描述的是请求体参数
class Book(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="图书名称")
    author: str = Field(min_length=2, max_length=10, description="作者名称")
    publisher: str = Field("黑马出版社")
    price: float = Field(..., ge=0)


@app.post("/book")
async def create_book(book: Book):
    return book
