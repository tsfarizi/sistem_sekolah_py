from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import decode_token
from core.exceptions import UnauthorizedException, ForbiddenException
from features.auth.models import User

security = HTTPBearer()

CurrentUser = User


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> CurrentUser:
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise UnauthorizedException("Token tidak valid")
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if user is None:
        raise UnauthorizedException("User tidak ditemukan")
    return user


def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if current_user.role != "admin":
        raise ForbiddenException("Akses ditolak")
    return current_user


def require_any_role(*roles: str):
    def _check(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in roles:
            raise ForbiddenException("Akses ditolak")
        return current_user
    return _check
