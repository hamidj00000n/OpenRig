from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    full_name: str
    preferred_language: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    slug: str = Field(min_length=3, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class OrganizationRead(BaseModel):
    id: str
    name: str
    slug: str
    role: str
    created_at: datetime


class OrganizationList(BaseModel):
    items: list[OrganizationRead]


class OrganizationMemberRoleUpdate(BaseModel):
    role: Literal["admin", "manager", "member", "owner"]


class OrganizationMemberRead(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    joined_at: datetime


class OrganizationMemberList(BaseModel):
    items: list[OrganizationMemberRead]


class InvitationCreate(BaseModel):
    email: EmailStr
    role: Literal["admin", "manager", "member"] = "member"


class InvitationRead(BaseModel):
    id: str
    email: EmailStr
    role: str
    status: str
    expires_at: datetime
    created_at: datetime


class InvitationCreated(InvitationRead):
    token: str


class InvitationList(BaseModel):
    items: list[InvitationRead]


class InvitationAccept(BaseModel):
    token: str = Field(min_length=32, max_length=128)

class PermissionRead(BaseModel):
    role: Literal["admin", "manager", "member"]
    module: str
    can_view: bool
    can_create: bool
    can_update: bool
    can_delete: bool

class PermissionUpdate(BaseModel):
    role: Literal["admin", "manager", "member"]
    module: Literal["rigs", "equipment", "warehouse", "maintenance", "procurement", "reports"]
    can_view: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class PermissionList(BaseModel):
    items: list[PermissionRead]

class AuditLogRead(BaseModel):
    id: str
    actor_user_id: str | None
    action: str
    target_type: str
    target_id: str | None
    details: str
    created_at: datetime

class AuditLogList(BaseModel):
    items: list[AuditLogRead]
