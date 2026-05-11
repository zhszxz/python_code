from fastapi import FastAPI, HTTPException, Depends
from fastapi.params import Query

app = FastAPI()


# ==================== FastAPI  异常响应====================

# 案例：按id查询新闻，若没查到抛出异常
@app.get("/news/detail/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {"id": id, "message": f"这是第{id}条新闻"}


# ==================== FastAPI 中间件 ====================
# 洋葱模型
# 多个中间件自底向上执行
@app.middleware("http")
async def middleware1(request, call_next):
    print("start - 中间件1")
    response = await call_next(request)
    print("end - 中间件1")
    return response


@app.middleware("http")
async def middleware2(request, call_next):
    print("start - 中间件2")
    response = await call_next(request)
    print("end - 中间件2")
    return response


# ==================== FastAPI 依赖注入 ====================
# 封装分页查询通用逻辑
async def get_page_items(
        skip: int = Query(0, description="跳过的记录数", ge=0),
        limit: int = Query(10, le=100, description="返回的记录数")):
    return {"skip": skip, "limit": limit}


@app.get("/news/list")
async def news_list(params=Depends(get_page_items)):
    return params


@app.get("/user/list")
async def user_list():
    return {"msg": "hello"}
