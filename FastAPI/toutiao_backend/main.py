from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import news

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 添加路由
app.include_router(news.router)
