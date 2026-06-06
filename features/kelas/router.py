from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.kelas.schemas import KelasCreate, KelasUpdate, KelasResponse
from features.kelas.service import list_kelas, detail_kelas, create_kelas, update_kelas, delete_kelas

router = APIRouter(prefix="/api/kelas", tags=["Kelas"])


@router.get("", response_model=list[KelasResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_kelas(db)


@router.get("/{id}", response_model=KelasResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detail_kelas(db, id)


@router.post("", response_model=KelasResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: KelasCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return create_kelas(db, data)


@router.put("/{id}", response_model=KelasResponse)
def update(
    id: int,
    data: KelasUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return update_kelas(db, id, data)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    delete_kelas(db, id)
    return {"message": "Kelas berhasil dihapus"}
