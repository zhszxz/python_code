from fastapi import FastAPI, Path

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


# 参数校验: id 必须在0到100之间
@app.get("/book/{id}")
async def get_book(id: int = Path(..., ge=0, lt=101)):
    return {"id": id, "message": f"这是第{id}本书"}


# 参数校验: name 长度必须在 2 到 10 之间
@app.get("/author/{name}")
async def author(name: str = Path(..., min_length=2, max_length=10)):
    return {"name": name, "message": f"作者名字是{name}"}
