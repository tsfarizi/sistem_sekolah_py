from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.laporan.schemas import LaporanKelasResponse, LaporanSiswaResponse
from features.laporan.service import laporan_by_kelas, laporan_by_siswa

router = APIRouter(prefix="/api/laporan", tags=["Laporan"])


@router.get("", response_model=list[LaporanKelasResponse])
def get_laporan_kelas(
    kelas_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return laporan_by_kelas(db, kelas_id=kelas_id)


@router.get("/siswa/{nis}", response_model=LaporanSiswaResponse)
def get_laporan_siswa(
    nis: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return laporan_by_siswa(db, nis)
