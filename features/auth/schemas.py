from pydantic import BaseModel, ConfigDict, field_validator


class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
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
    role: str
    nama: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse
