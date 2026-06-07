from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user, require_any_role, require_admin, CurrentUser
from core.schemas import Message
from features.nilai.schemas import NilaiCreate, NilaiUpdate, NilaiResponse
from features.nilai.service import (
    list_nilai,
    detail_nilai,
    create_nilai,
    update_nilai,
    list_nilai_by_siswa,
    delete_nilai,
)

router = APIRouter(prefix="/api/nilai", tags=["Nilai"])


@router.get("", response_model=list[NilaiResponse])
def get_all(
    kelas_id: int | None = Query(None),
    mata_pelajaran_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return list_nilai(db, current_user, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id)


@router.get("/siswa/{nis}", response_model=list[NilaiResponse])
def get_by_siswa(
    nis: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return list_nilai_by_siswa(db, nis, current_user)


@router.get("/{id}", response_model=NilaiResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return detail_nilai(db, id)


@router.post("", response_model=NilaiResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: NilaiCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_any_role("admin", "guru")),
):
    return create_nilai(db, data, current_user)


@router.put("/{id}", response_model=NilaiResponse)
def update(
    id: int,
    data: NilaiUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_any_role("admin", "guru")),
):
    return update_nilai(db, id, data, current_user)


@router.delete("/{id}", response_model=Message)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
):
    delete_nilai(db, id)
    return {"message": "Nilai berhasil dihapus"}
