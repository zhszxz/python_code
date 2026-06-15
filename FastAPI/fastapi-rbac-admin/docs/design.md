# 项目设计文档：FastAPI RBAC 用户权限管理系统

## 1. 系统目标

本项目用于学习 FastAPI 实战开发，目标是实现一个可以本机运行、前后端联调、接口级鉴权完整闭环的 RBAC 权限管理系统。

核心能力：

- 用户登录、JWT 签发和当前用户查询。
- 用户、角色、权限三类资源的后台维护。
- 用户绑定多个角色，角色绑定多个权限。
- 接口通过 `require_permission("权限标识")` 做权限拦截。
- 前端根据当前用户权限控制菜单和操作按钮展示。

## 2. RBAC 模型

RBAC 是 Role-Based Access Control，即基于角色的访问控制。

```text
用户 User  <->  角色 Role  <->  权限 Permission
```

- 用户不直接拥有接口权限。
- 用户通过角色间接获得权限。
- 一个用户可以拥有多个角色。
- 一个角色可以绑定多个权限。
- 权限使用字符串标识，例如 `user:read`、`role:update`。

## 3. 数据表设计

| 表名 | 说明 |
| --- | --- |
| `users` | 用户表，保存用户名、昵称、密码哈希和启用状态 |
| `roles` | 角色表，保存角色编码、名称和描述 |
| `permissions` | 权限表，保存权限标识、名称、分组和描述 |
| `user_roles` | 用户角色关联表 |
| `role_permissions` | 角色权限关联表 |

## 4. 后端分层

| 层级 | 目录 | 职责 |
| --- | --- | --- |
| 路由层 | `app/api` | 定义 HTTP 接口、中文摘要、依赖鉴权 |
| Schema 层 | `app/schemas` | 请求参数和响应数据结构 |
| Service 层 | `app/services` | 业务逻辑、查询封装、权限汇总 |
| Model 层 | `app/models` | SQLAlchemy ORM 模型 |
| Core 层 | `app/core` | 配置、数据库、JWT、密码哈希 |
| Common 层 | `app/common` | 统一响应结构 |

## 5. 鉴权流程

1. 前端提交用户名和密码到 `/api/v1/auth/login`。
2. 后端验证密码哈希，签发 JWT。
3. 前端把 Token 保存到 `localStorage`。
4. Axios 请求拦截器自动添加 `Authorization: Bearer <token>`。
5. 后端 `get_current_user` 解析 Token 并加载用户角色权限。
6. 需要授权的接口声明 `Depends(require_permission("user:read"))`。
7. 当前用户缺少权限时返回 403。

## 6. 前端交互设计

前端使用 Vue3 + Element Plus 实现管理后台：

- 登录页：使用演示账号登录。
- 控制台：展示当前用户、角色和权限数量。
- 用户管理：用户列表、新增、编辑、删除、分配角色。
- 角色管理：角色列表、新增、编辑、删除、分配权限。
- 权限管理：权限列表、新增、编辑、删除。

菜单和按钮通过 `auth.has("权限标识")` 判断是否展示。这个判断只用于改善体验，真正的安全边界仍然在后端接口鉴权。

## 7. 接口清单

| 模块 | 接口 |
| --- | --- |
| 登录认证 | `POST /api/v1/auth/login`、`GET /api/v1/auth/me` |
| 用户管理 | `GET/POST /api/v1/users`、`PUT/DELETE /api/v1/users/{id}` |
| 角色管理 | `GET/POST /api/v1/roles`、`PUT/DELETE /api/v1/roles/{id}` |
| 权限管理 | `GET/POST /api/v1/permissions`、`PUT/DELETE /api/v1/permissions/{id}` |

## 8. 可扩展方向

- 引入 Alembic 管理数据库迁移。
- 增加菜单表，把按钮权限和路由菜单分离。
- 增加操作日志、登录日志和审计记录。
- 用 MySQL 或 PostgreSQL 替换 SQLite。
- 增加 pytest 自动化测试和 CI。
