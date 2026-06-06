from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.auth.schemas import (
    LoginRequest, LoginResponse,
    ChangePasswordRequest, ResetPasswordRequest,
    UserCreate, UserUpdate, UserResponse,
)
from features.auth.service import (
    authenticate, change_password, reset_password,
    list_users, get_user, create_user, update_user, delete_user,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])
user_router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate(db, data)


@router.put("/change-password")
def change_password_endpoint(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    change_password(db, current_user, data)
    return {"message": "Password berhasil diubah"}


@router.put("/reset-password/{user_id}")
def reset_password_endpoint(
    user_id: int,
    data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    reset_password(db, user_id, data.new_password)
    return {"message": "Password berhasil direset"}


@user_router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return list_users(db)


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return get_user(db, user_id)


@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return create_user(db, data)


@user_router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return update_user(db, user_id, data)


@user_router.delete("/{user_id}")
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    delete_user(db, user_id)
    return {"message": "User berhasil dihapus"}
