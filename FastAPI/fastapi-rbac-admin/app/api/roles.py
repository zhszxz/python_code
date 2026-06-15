from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.common.response import ApiResponse, ok
from app.core.database import get_db
from app.schemas.rbac import RoleCreate, RoleUpdate
from app.services import rbac


router = APIRouter(prefix="/roles", tags=["角色管理"])


@router.get("", response_model=ApiResponse, summary="查询角色列表", dependencies=[Depends(require_permission("role:read"))])
def list_roles(db: Session = Depends(get_db)) -> ApiResponse:
    """角色列表接口：返回角色以及角色已绑定的权限集合。"""

    return ok([rbac.role_to_read(role) for role in rbac.list_roles(db)])


@router.post("", response_model=ApiResponse, summary="创建角色", dependencies=[Depends(require_permission("role:create"))])
def create_role(payload: RoleCreate, db: Session = Depends(get_db)) -> ApiResponse:
    """创建角色接口：创建角色并可一次性绑定权限 ID 列表。"""

    return ok(rbac.role_to_read(rbac.create_role(db, payload)), "角色创建成功")


@router.put("/{role_id}", response_model=ApiResponse, summary="更新角色", dependencies=[Depends(require_permission("role:update"))])
def update_role(role_id: int, payload: RoleUpdate, db: Session = Depends(get_db)) -> ApiResponse:
    """更新角色接口：修改角色展示信息，并重新分配权限。"""

    return ok(rbac.role_to_read(rbac.update_role(db, role_id, payload)), "角色更新成功")


@router.delete("/{role_id}", response_model=ApiResponse, summary="删除角色", dependencies=[Depends(require_permission("role:delete"))])
def delete_role(role_id: int, db: Session = Depends(get_db)) -> ApiResponse:
    """删除角色接口：删除角色并级联清理用户、权限关联关系。"""

    rbac.delete_role(db, role_id)
    return ok(message="角色删除成功")
