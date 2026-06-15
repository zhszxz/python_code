from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PermissionBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=2, max_length=80)
    group: str = "default"
    description: str = ""


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None
    group: str | None = None
    description: str | None = None


class PermissionRead(PermissionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    label: str = Field(..., min_length=2, max_length=80)
    description: str = ""


class RoleCreate(RoleBase):
    permission_ids: list[int] = []


class RoleUpdate(BaseModel):
    label: str | None = None
    description: str | None = None
    permission_ids: list[int] | None = None


class RoleRead(RoleBase):
    id: int
    permissions: list[PermissionRead] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nickname: str = Field(..., min_length=2, max_length=80)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)
    role_ids: list[int] = []


class UserUpdate(BaseModel):
    nickname: str | None = None
    password: str | None = Field(default=None, min_length=6, max_length=50)
    is_active: bool | None = None
    role_ids: list[int] | None = None


class UserRead(UserBase):
    id: int
    roles: list[RoleRead] = []
    permissions: list[str] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class IdsRequest(BaseModel):
    ids: list[int]
