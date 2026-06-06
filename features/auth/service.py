from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.auth.models import User
from features.auth.schemas import LoginRequest, LoginResponse, UserResponse, ChangePasswordRequest, UserCreate, UserUpdate
from core.security import verify_password, create_access_token, hash_password


def authenticate(db: Session, data: LoginRequest) -> LoginResponse:
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )
    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return LoginResponse(
        token=token,
        user=UserResponse.model_validate(user),
    )


def change_password(db: Session, current_user: User, data: ChangePasswordRequest) -> None:
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password lama salah"
        )
    current_user.password_hash = hash_password(data.new_password)
    db.commit()


def reset_password(db: Session, user_id: int, new_password: str) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan"
        )
    user.password_hash = hash_password(new_password)
    db.commit()


def list_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan"
        )
    return user


def create_user(db: Session, data: UserCreate) -> User:
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah digunakan"
        )
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role=data.role,
        nama=data.nama,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan"
        )
    if data.username is not None:
        existing = db.query(User).filter(User.username == data.username, User.id != user_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah digunakan"
            )
        user.username = data.username
    if data.password is not None:
        user.password_hash = hash_password(data.password)
    if data.role is not None:
        user.role = data.role
    if data.nama is not None:
        user.nama = data.nama
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User tidak ditemukan"
        )
    db.delete(user)
    db.commit()
