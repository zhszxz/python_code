from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_password_hash, verify_password
from app.models import Permission, Role, User
from app.schemas.rbac import PermissionCreate, PermissionUpdate, RoleCreate, RoleUpdate, UserCreate, UserUpdate


def permission_codes(user: User) -> list[str]:
    """汇总用户所有角色绑定的权限标识，供接口鉴权和前端按钮控制使用。"""

    codes = {permission.code for role in user.roles for permission in role.permissions}
    return sorted(codes)


def permission_to_read(permission: Permission) -> dict:
    return {
        "id": permission.id,
        "code": permission.code,
        "name": permission.name,
        "group": permission.group,
        "description": permission.description,
        "created_at": permission.created_at,
    }


def role_to_read(role: Role) -> dict:
    return {
        "id": role.id,
        "name": role.name,
        "label": role.label,
        "description": role.description,
        "permissions": [permission_to_read(permission) for permission in role.permissions],
        "created_at": role.created_at,
    }


def user_to_read(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "is_active": user.is_active,
        "roles": [role_to_read(role) for role in user.roles],
        "permissions": permission_codes(user),
        "created_at": user.created_at,
    }


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = (
        select(User)
        .where(User.username == username)
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    return db.scalar(stmt)


def get_user(db: Session, user_id: int) -> User:
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    user = db.scalar(stmt)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户已被禁用")
    return user


def list_users(db: Session) -> list[User]:
    stmt = select(User).options(selectinload(User.roles).selectinload(Role.permissions)).order_by(User.id)
    return list(db.scalars(stmt).all())


def create_user(db: Session, payload: UserCreate) -> User:
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已存在")
    roles = list(db.scalars(select(Role).where(Role.id.in_(payload.role_ids))).all()) if payload.role_ids else []
    user = User(
        username=payload.username,
        nickname=payload.nickname,
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active,
        roles=roles,
    )
    db.add(user)
    db.commit()
    return get_user(db, user.id)


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = get_user(db, user_id)
    if payload.nickname is not None:
        user.nickname = payload.nickname
    if payload.password:
        user.hashed_password = get_password_hash(payload.password)
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.role_ids is not None:
        user.roles = list(db.scalars(select(Role).where(Role.id.in_(payload.role_ids))).all())
    db.commit()
    return get_user(db, user.id)


def delete_user(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()


def list_roles(db: Session) -> list[Role]:
    stmt = select(Role).options(selectinload(Role.permissions)).order_by(Role.id)
    return list(db.scalars(stmt).all())


def get_role(db: Session, role_id: int) -> Role:
    role = db.scalar(select(Role).where(Role.id == role_id).options(selectinload(Role.permissions)))
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return role


def create_role(db: Session, payload: RoleCreate) -> Role:
    if db.scalar(select(Role).where(Role.name == payload.name)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="角色编码已存在")
    permissions = list(db.scalars(select(Permission).where(Permission.id.in_(payload.permission_ids))).all())
    role = Role(name=payload.name, label=payload.label, description=payload.description, permissions=permissions)
    db.add(role)
    db.commit()
    return get_role(db, role.id)


def update_role(db: Session, role_id: int, payload: RoleUpdate) -> Role:
    role = get_role(db, role_id)
    if payload.label is not None:
        role.label = payload.label
    if payload.description is not None:
        role.description = payload.description
    if payload.permission_ids is not None:
        role.permissions = list(db.scalars(select(Permission).where(Permission.id.in_(payload.permission_ids))).all())
    db.commit()
    return get_role(db, role.id)


def delete_role(db: Session, role_id: int) -> None:
    role = get_role(db, role_id)
    db.delete(role)
    db.commit()


def list_permissions(db: Session) -> list[Permission]:
    return list(db.scalars(select(Permission).order_by(Permission.group, Permission.id)).all())


def get_permission(db: Session, permission_id: int) -> Permission:
    permission = db.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="权限不存在")
    return permission


def create_permission(db: Session, payload: PermissionCreate) -> Permission:
    if db.scalar(select(Permission).where(Permission.code == payload.code)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="权限标识已存在")
    permission = Permission(**payload.model_dump())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def update_permission(db: Session, permission_id: int, payload: PermissionUpdate) -> Permission:
    permission = get_permission(db, permission_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(permission, key, value)
    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission_id: int) -> None:
    permission = get_permission(db, permission_id)
    db.delete(permission)
    db.commit()
