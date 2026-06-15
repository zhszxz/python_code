from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import User
from app.services.rbac import get_user, permission_codes


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """解析 Bearer Token，返回当前登录用户。"""

    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录已过期，请重新登录")
    return get_user(db, int(user_id))


def require_permission(code: str) -> Callable[[User], User]:
    """接口级 RBAC 依赖：当前用户必须拥有指定权限标识。"""

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if code not in permission_codes(current_user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"缺少权限：{code}")
        return current_user

    return checker
