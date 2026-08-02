from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class CreateUserRequest(BaseModel):
    business_name: str
    full_name: str
    email: EmailStr
    phone: str  
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    profile_image: str | None = None

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str
    profile_image: str | None
    is_email_verified: bool
    is_phone_verified: bool
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: datetime




class TokenResponse(BaseModel):
    access_token: str
    role: str
    tenant: TenantInfoResponse


class CurrentUserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    tenant_id: UUID
    tenant_name: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
    )

class TenantInfoResponse(BaseModel):
    id: UUID
    name: str