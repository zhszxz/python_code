from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.common.response import ApiResponse, ok
from app.core.database import get_db
from app.schemas.rbac import PermissionCreate, PermissionUpdate
from app.services import rbac


router = APIRouter(prefix="/permissions", tags=["权限管理"])


@router.get("", response_model=ApiResponse, summary="查询权限列表", dependencies=[Depends(require_permission("permission:read"))])
def list_permissions(db: Session = Depends(get_db)) -> ApiResponse:
    """权限列表接口：查询系统全部权限标识，供角色授权时勾选。"""

    return ok([rbac.permission_to_read(permission) for permission in rbac.list_permissions(db)])


@router.post("", response_model=ApiResponse, summary="创建权限", dependencies=[Depends(require_permission("permission:create"))])
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)) -> ApiResponse:
    """创建权限接口：新增一个接口级权限标识，例如 user:read。"""

    return ok(rbac.permission_to_read(rbac.create_permission(db, payload)), "权限创建成功")


@router.put("/{permission_id}", response_model=ApiResponse, summary="更新权限", dependencies=[Depends(require_permission("permission:update"))])
def update_permission(permission_id: int, payload: PermissionUpdate, db: Session = Depends(get_db)) -> ApiResponse:
    """更新权限接口：修改权限名称、分组和说明。"""

    return ok(rbac.permission_to_read(rbac.update_permission(db, permission_id, payload)), "权限更新成功")


@router.delete("/{permission_id}", response_model=ApiResponse, summary="删除权限", dependencies=[Depends(require_permission("permission:delete"))])
def delete_permission(permission_id: int, db: Session = Depends(get_db)) -> ApiResponse:
    """删除权限接口：删除权限并级联清理角色权限关联。"""

    rbac.delete_permission(db, permission_id)
    return ok(message="权限删除成功")
