from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.auth.schemas import LoginRequest, LoginResponse, ChangePasswordRequest, ResetPasswordRequest
from features.auth.service import authenticate, change_password, reset_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])


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
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    reset_password(db, user_id, data.new_password)
    return {"message": "Password berhasil direset"}
