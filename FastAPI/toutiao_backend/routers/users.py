"""
用户模块控制器
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from crud import users
from utils.result import Result

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    """
    print(user_data)
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return Result.success(message="注册成功", data=data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return Result.success(message="登录成功", data=response_data)

@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))
