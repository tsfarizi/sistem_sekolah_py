from sqlalchemy.orm import Session
from features.auth.models import User
from features.auth.schemas import LoginRequest, LoginResponse, UserResponse, ChangePasswordRequest, UserCreate, UserUpdate
from features.auth.repository import (
    get_user_by_username,
    get_user_by_id,
    get_all_users,
    check_username_conflict,
    create_user as repo_create_user,
    update_user as repo_update_user,
    delete_user as repo_delete_user,
)
from core.security import verify_password, create_access_token, hash_password
from core.exceptions import UnauthorizedException, NotFoundException, BadRequestException


def authenticate(db: Session, data: LoginRequest) -> LoginResponse:
    user = get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.password_hash):
        raise UnauthorizedException("Username atau password salah")
    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return LoginResponse(
        token=token,
        user=UserResponse.model_validate(user),
    )


def change_password(db: Session, current_user: User, data: ChangePasswordRequest) -> None:
    if not verify_password(data.old_password, current_user.password_hash):
        raise BadRequestException("Password lama salah")
    current_user.password_hash = hash_password(data.new_password)
    repo_update_user(db, current_user)


def reset_password(db: Session, user_id: int, new_password: str) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User tidak ditemukan")
    user.password_hash = hash_password(new_password)
    repo_update_user(db, user)


def list_users(db: Session) -> list[User]:
    return get_all_users(db)


def get_user(db: Session, user_id: int) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User tidak ditemukan")
    return user


def create_user(db: Session, data: UserCreate) -> User:
    existing = check_username_conflict(db, data.username)
    if existing:
        raise BadRequestException("Username sudah digunakan")
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role=data.role,
        nama=data.nama,
    )
    return repo_create_user(db, user)


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User tidak ditemukan")
    if data.username is not None:
        existing = check_username_conflict(db, data.username, exclude_id=user_id)
        if existing:
            raise BadRequestException("Username sudah digunakan")
        user.username = data.username
    if data.password is not None:
        user.password_hash = hash_password(data.password)
    if data.role is not None:
        user.role = data.role
    if data.nama is not None:
        user.nama = data.nama
    return repo_update_user(db, user)


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User tidak ditemukan")
    repo_delete_user(db, user)
