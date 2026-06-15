from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.common.response import ApiResponse, ok
from app.core.database import get_db
from app.schemas.rbac import UserCreate, UserUpdate
from app.services import rbac


router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", response_model=ApiResponse, summary="查询用户列表", dependencies=[Depends(require_permission("user:read"))])
def list_users(db: Session = Depends(get_db)) -> ApiResponse:
    """用户列表接口：查询所有用户及其角色、权限，用于后台表格展示。"""

    return ok([rbac.user_to_read(user) for user in rbac.list_users(db)])


@router.post("", response_model=ApiResponse, summary="创建用户", dependencies=[Depends(require_permission("user:create"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> ApiResponse:
    """创建用户接口：写入用户基础信息，并可同步绑定角色。"""

    return ok(rbac.user_to_read(rbac.create_user(db, payload)), "用户创建成功")


@router.put("/{user_id}", response_model=ApiResponse, summary="更新用户", dependencies=[Depends(require_permission("user:update"))])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> ApiResponse:
    """更新用户接口：支持修改昵称、密码、启用状态和角色关系。"""

    return ok(rbac.user_to_read(rbac.update_user(db, user_id, payload)), "用户更新成功")


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse, summary="删除用户", dependencies=[Depends(require_permission("user:delete"))])
def delete_user(user_id: int, db: Session = Depends(get_db)) -> ApiResponse:
    """删除用户接口：删除用户并级联清理用户角色关联。"""

    rbac.delete_user(db, user_id)
    return ok(message="用户删除成功")
