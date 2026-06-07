from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user, require_any_role, CurrentUser
from features.laporan.schemas import LaporanKelasResponse, LaporanSiswaResponse
from features.laporan.service import laporan_by_kelas, laporan_by_siswa

router = APIRouter(prefix="/api/laporan", tags=["Laporan"])


@router.get("", response_model=list[LaporanKelasResponse])
def get_laporan_kelas(
    kelas_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_any_role("admin", "guru")),
):
    return laporan_by_kelas(db, kelas_id=kelas_id, current_user=current_user)


@router.get("/siswa/{nis}", response_model=LaporanSiswaResponse)
def get_laporan_siswa(
    nis: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_any_role("admin", "guru")),
):
    return laporan_by_siswa(db, nis, current_user=current_user)
