from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, field_validator, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str

    @field_validator("new_password")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password baru minimal 6 karakter")
        return v


class ResetPasswordRequest(BaseModel):
    new_password: str

    @field_validator("new_password")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password baru minimal 6 karakter")
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    role: Literal["admin", "guru", "siswa"]
    nama: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    nama: str

    @field_validator("password")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password minimal 6 karakter")
        return v

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        if v not in ("admin", "guru", "siswa"):
            raise ValueError("Role harus admin, guru, atau siswa")
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    nama: Optional[str] = None

    @field_validator("password")
    @classmethod
    def min_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) < 6:
            raise ValueError("Password minimal 6 karakter")
        return v

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("admin", "guru", "siswa"):
            raise ValueError("Role harus admin, guru, atau siswa")
        return v
