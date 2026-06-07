from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user, require_admin, CurrentUser
from core.schemas import Message
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
    current_user: CurrentUser = Depends(get_current_user),
):
    return list_siswa(db, kelas_id=kelas_id)


@router.get("/{nis}", response_model=SiswaWithNilaiResponse)
def get_by_nis(
    nis: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return detail_siswa(db, nis)


@router.post("", response_model=SiswaResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: SiswaCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    return create_new_siswa(db, data)


@router.put("/{nis}", response_model=SiswaResponse)
def update(
    nis: str,
    data: SiswaUpdate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    return update_existing_siswa(db, nis, data)


@router.delete("/{nis}", response_model=Message)
def delete(
    nis: str,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    delete_existing_siswa(db, nis)
    return {"message": "Siswa berhasil dihapus"}
