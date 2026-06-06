from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.nilai.schemas import NilaiCreate, NilaiUpdate, NilaiResponse
from features.nilai.service import (
    list_nilai,
    detail_nilai,
    create_new_nilai,
    update_existing_nilai,
    list_nilai_by_siswa_service,
)
from features.nilai.repository import get_nilai_by_id, delete_nilai as repo_delete_nilai

router = APIRouter(prefix="/api/nilai", tags=["Nilai"])


@router.get("", response_model=list[NilaiResponse])
def get_all(
    kelas_id: int | None = Query(None),
    mata_pelajaran_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "guru", "siswa"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return list_nilai(db, current_user, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id)


@router.get("/siswa/{nis}", response_model=list[NilaiResponse])
def get_by_siswa(
    nis: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_nilai_by_siswa_service(db, nis, current_user)


@router.get("/{id}", response_model=NilaiResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detail_nilai(db, id)


@router.post("", response_model=NilaiResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: NilaiCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "guru"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return create_new_nilai(db, data)


@router.put("/{id}", response_model=NilaiResponse)
def update(
    id: int,
    data: NilaiUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["admin", "guru"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return update_existing_nilai(db, id, data)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    nilai = get_nilai_by_id(db, id)
    if not nilai:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nilai tidak ditemukan"
        )
    repo_delete_nilai(db, nilai)
    return {"message": "Nilai berhasil dihapus"}
