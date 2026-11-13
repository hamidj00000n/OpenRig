from datetime import datetime
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
