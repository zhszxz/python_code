# FastAPI RBAC Admin

这是一个面向 FastAPI 学习的前后端完整 RBAC 用户权限管理系统。项目覆盖登录认证、JWT、SQLAlchemy ORM、多对多关系、接口级权限拦截、Vue 管理后台和 Hexo 实战笔记。

## 技术栈

- 后端：FastAPI、SQLAlchemy 2.x、Pydantic、JWT、SQLite
- 前端：Vue3、Vite、Element Plus、Pinia、Axios
- 权限模型：用户关联角色，角色关联权限，接口通过权限标识控制访问

## 后端启动

```powershell
cd D:\pycharm_workspace\python_code\FastAPI\fastapi-rbac-admin
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\init_db.py
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

启动后访问：

- 接口文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/

## 前端启动

```powershell
cd D:\pycharm_workspace\python_code\FastAPI\fastapi-rbac-admin\frontend
npm install
npm run dev
```

前端默认地址：http://127.0.0.1:5173

## 演示账号

| 用户名 | 密码 | 角色 |
| --- | --- | --- |
| admin | admin123 | 系统管理员 |
| editor | editor123 | 运营编辑 |
| viewer | viewer123 | 只读访客 |

## 核心接口

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/login` | 登录获取 Token | 无 |
| GET | `/api/v1/auth/me` | 当前用户信息 | 登录 |
| GET | `/api/v1/users` | 用户列表 | `user:read` |
| POST | `/api/v1/users` | 创建用户 | `user:create` |
| PUT | `/api/v1/users/{id}` | 更新用户 | `user:update` |
| DELETE | `/api/v1/users/{id}` | 删除用户 | `user:delete` |
| GET | `/api/v1/roles` | 角色列表 | `role:read` |
| POST | `/api/v1/roles` | 创建角色 | `role:create` |
| GET | `/api/v1/permissions` | 权限列表 | `permission:read` |

## 学习重点

1. FastAPI 的路由、依赖注入和 Swagger 文档。
2. SQLAlchemy 2.x 的声明式模型和多对多关系。
3. JWT 登录态与 Bearer Token 校验。
4. RBAC 的用户、角色、权限三层授权模型。
5. Vue 前端如何保存 Token、处理 401、按权限控制菜单和按钮。
