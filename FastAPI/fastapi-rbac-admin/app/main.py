from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import auth, permissions, roles, users
from app.core.config import settings


app = FastAPI(title=settings.app_name, description="基于 FastAPI 的 RBAC 用户权限管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常兜底：未处理异常统一返回固定 JSON，便于前端展示。"""

    return JSONResponse(status_code=500, content={"code": 500, "message": str(exc), "data": None})


@app.get("/", summary="健康检查")
def health_check() -> dict[str, str]:
    """健康检查接口：确认服务已经正常启动。"""

    return {"message": "FastAPI RBAC Admin is running"}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(roles.router, prefix=settings.api_prefix)
app.include_router(permissions.router, prefix=settings.api_prefix)
