from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.common.response import ApiResponse, ok
from app.core.database import get_db
from app.core.security import create_access_token
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.rbac import authenticate_user, user_to_read


router = APIRouter(prefix="/auth", tags=["登录认证"])


@router.post("/login", response_model=ApiResponse, summary="账号密码登录")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse:
    """登录接口：校验用户名密码，成功后返回 JWT 令牌。"""

    user = authenticate_user(db, payload.username, payload.password)
    token = create_access_token(str(user.id))
    return ok(TokenResponse(access_token=token).model_dump(), "登录成功")


@router.get("/me", response_model=ApiResponse, summary="获取当前登录用户")
def current_user_profile(current_user: User = Depends(get_current_user)) -> ApiResponse:
    """当前用户接口：返回用户基础信息、角色和权限标识列表。"""

    return ok(user_to_read(current_user))
