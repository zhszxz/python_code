from fastapi import FastAPI, HTTPException

app = FastAPI()


# ==================== FastAPI  ====================

# 案例：按id查询新闻，若没查到抛出异常
@app.get("/news/{id}")
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
