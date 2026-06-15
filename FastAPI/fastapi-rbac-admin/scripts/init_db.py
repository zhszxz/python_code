import sys
from pathlib import Path

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import Permission, Role, User


PERMISSIONS = [
    ("user:read", "查看用户", "用户管理"),
    ("user:create", "创建用户", "用户管理"),
    ("user:update", "更新用户", "用户管理"),
    ("user:delete", "删除用户", "用户管理"),
    ("role:read", "查看角色", "角色管理"),
    ("role:create", "创建角色", "角色管理"),
    ("role:update", "更新角色", "角色管理"),
    ("role:delete", "删除角色", "角色管理"),
    ("permission:read", "查看权限", "权限管理"),
    ("permission:create", "创建权限", "权限管理"),
    ("permission:update", "更新权限", "权限管理"),
    ("permission:delete", "删除权限", "权限管理"),
]


def main() -> None:
    """初始化数据库表和演示账号，可重复执行。"""

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        permission_map = {}
        for code, name, group in PERMISSIONS:
            permission = db.scalar(select(Permission).where(Permission.code == code))
            if not permission:
                permission = Permission(code=code, name=name, group=group, description=f"{name}接口权限")
                db.add(permission)
            permission_map[code] = permission
        db.flush()

        admin_role = db.scalar(select(Role).where(Role.name == "admin")) or Role(
            name="admin", label="系统管理员", description="拥有全部管理权限"
        )
        editor_role = db.scalar(select(Role).where(Role.name == "editor")) or Role(
            name="editor", label="运营编辑", description="可查看并维护用户、角色基础信息"
        )
        viewer_role = db.scalar(select(Role).where(Role.name == "viewer")) or Role(
            name="viewer", label="只读访客", description="仅可查看后台数据"
        )
        admin_role.permissions = list(permission_map.values())
        editor_role.permissions = [p for code, p in permission_map.items() if code.endswith(":read") or code in {"user:update"}]
        viewer_role.permissions = [p for code, p in permission_map.items() if code.endswith(":read")]
        db.add_all([admin_role, editor_role, viewer_role])
        db.flush()

        users = [
            ("admin", "管理员", "admin123", [admin_role]),
            ("editor", "编辑用户", "editor123", [editor_role]),
            ("viewer", "访客用户", "viewer123", [viewer_role]),
        ]
        for username, nickname, password, roles in users:
            user = db.scalar(select(User).where(User.username == username))
            if not user:
                user = User(username=username, nickname=nickname, hashed_password=get_password_hash(password), roles=roles)
                db.add(user)
            else:
                user.roles = roles
        db.commit()
        print("数据库初始化完成：admin/admin123, editor/editor123, viewer/viewer123")
    finally:
        db.close()


if __name__ == "__main__":
    main()
