from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.nilai.models import Nilai
from features.nilai.repository import (
    get_all_nilai,
    get_nilai_by_id,
    get_nilai_by_siswa,
    create_nilai as repo_create_nilai,
    update_nilai as repo_update_nilai,
    delete_nilai as repo_delete_nilai,
)
from features.nilai.schemas import NilaiCreate, NilaiUpdate
from features.nilai.utils import validasi_nilai
from features.auth.models import User
from features.siswa.models import Siswa
from features.guru_mengajar.models import GuruMengajar


def list_nilai(db: Session, current_user: User, kelas_id: int | None = None, mata_pelajaran_id: int | None = None) -> list[Nilai]:
    query = db.query(Nilai)
    if current_user.role == "siswa":
        siswa = db.query(Siswa).filter(Siswa.user_id == current_user.id).first()
        if siswa:
            query = query.filter(Nilai.nis == siswa.nis)
        else:
            return []
    if kelas_id or mata_pelajaran_id:
        query = query.join(Nilai.guru_mengajar)
        if kelas_id:
            query = query.filter(GuruMengajar.kelas_id == kelas_id)
        if mata_pelajaran_id:
            query = query.filter(GuruMengajar.mata_pelajaran_id == mata_pelajaran_id)
    return query.all()


def detail_nilai(db: Session, nilai_id: int) -> Nilai:
    nilai = get_nilai_by_id(db, nilai_id)
    if not nilai:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nilai tidak ditemukan"
        )
    return nilai


def create_new_nilai(db: Session, data: NilaiCreate, current_user: User) -> Nilai:
    if not validasi_nilai(data.tugas):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai tugas harus 0-100"
        )
    if not validasi_nilai(data.uts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai UTS harus 0-100"
        )
    if not validasi_nilai(data.uas):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai UAS harus 0-100"
        )
    siswa = db.query(Siswa).filter(Siswa.nis == data.nis).first()
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Siswa tidak ditemukan"
        )
    gm_query = db.query(GuruMengajar).filter(GuruMengajar.id == data.guru_mengajar_id)
    if current_user.role == "guru":
        if not current_user.guru:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Akun guru tidak valid"
            )
        gm_query = gm_query.filter(GuruMengajar.guru_id == current_user.guru.id)
    gm = gm_query.first()
    if not gm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Data guru mengajar tidak ditemukan"
        )
    nilai = Nilai(
        nis=data.nis,
        guru_mengajar_id=data.guru_mengajar_id,
        tugas=data.tugas,
        uts=data.uts,
        uas=data.uas,
        nilai_akhir=0.0,
        status="",
    )
    nilai.kalkulasi()
    return repo_create_nilai(db, nilai)


def update_existing_nilai(db: Session, nilai_id: int, data: NilaiUpdate, current_user: User) -> Nilai:
    nilai = get_nilai_by_id(db, nilai_id)
    if not nilai:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nilai tidak ditemukan"
        )
    if current_user.role == "guru":
        if not current_user.guru or nilai.guru_mengajar.guru_id != current_user.guru.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak berhak mengubah nilai ini"
            )
    if data.tugas is not None:
        if not validasi_nilai(data.tugas):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai tugas harus 0-100"
            )
        nilai.tugas = data.tugas
    if data.uts is not None:
        if not validasi_nilai(data.uts):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai UTS harus 0-100"
            )
        nilai.uts = data.uts
    if data.uas is not None:
        if not validasi_nilai(data.uas):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Nilai UAS harus 0-100"
            )
        nilai.uas = data.uas
    nilai.kalkulasi()
    return repo_update_nilai(db, nilai)


def list_nilai_by_siswa_service(db: Session, nis: str, current_user: User) -> list[Nilai]:
    siswa = db.query(Siswa).filter(Siswa.nis == nis).first()
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Siswa tidak ditemukan"
        )
    if current_user.role == "siswa":
        current_siswa = db.query(Siswa).filter(Siswa.user_id == current_user.id).first()
        if not current_siswa or current_siswa.nis != nis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
    return get_nilai_by_siswa(db, nis)
