from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.siswa.schemas import SiswaCreate, SiswaUpdate, SiswaResponse, SiswaWithNilaiResponse
from features.siswa.service import (
    list_siswa,
    detail_siswa,
    create_new_siswa,
    update_existing_siswa,
    delete_existing_siswa,
)

router = APIRouter(prefix="/api/siswa", tags=["Siswa"])


@router.get("", response_model=list[SiswaResponse])
def get_all(
    kelas_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "guru"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return list_siswa(db, kelas_id=kelas_id)


@router.get("/{nis}", response_model=SiswaWithNilaiResponse)
def get_by_nis(
    nis: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detail_siswa(db, nis)


@router.post("", response_model=SiswaResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: SiswaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return create_new_siswa(db, data)


@router.put("/{nis}", response_model=SiswaResponse)
def update(
    nis: str,
    data: SiswaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return update_existing_siswa(db, nis, data)


@router.delete("/{nis}")
def delete(
    nis: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    delete_existing_siswa(db, nis)
    return {"message": "Siswa berhasil dihapus"}
