from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ==========================================================
# User Schemas
# ==========================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"