from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.mata_pelajaran.schemas import MataPelajaranCreate, MataPelajaranUpdate, MataPelajaranResponse
from features.mata_pelajaran.service import list_mapel, detail_mapel, create_mapel, update_mapel, delete_mapel

router = APIRouter(prefix="/api/mata-pelajaran", tags=["Mata Pelajaran"])


@router.get("", response_model=list[MataPelajaranResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_mapel(db)


@router.get("/{id}", response_model=MataPelajaranResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detail_mapel(db, id)


@router.post("", response_model=MataPelajaranResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: MataPelajaranCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return create_mapel(db, data)


@router.put("/{id}", response_model=MataPelajaranResponse)
def update(
    id: int,
    data: MataPelajaranUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return update_mapel(db, id, data)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    delete_mapel(db, id)
    return {"message": "Mata pelajaran berhasil dihapus"}
