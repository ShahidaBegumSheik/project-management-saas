from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class RegisterOut(BaseModel):
    message: str
    email: EmailStr
    verification_required: bool = True
    verification_token: str | None = None


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenIn(BaseModel):
    refresh_token: str


class VerifyEmailOut(BaseModel):
    message: str


class UserMeOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    email_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
