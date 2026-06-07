from sqlalchemy.orm import Session
from core.dependencies import CurrentUser
from features.nilai.models import Nilai
from features.nilai.repository import (
    get_nilai_by_id,
    get_nilai_by_siswa,
    get_nilai_filtered,
    get_siswa_by_nis,
    get_siswa_by_user_id,
    get_guru_mengajar_by_id,
    get_guru_mengajar_by_id_and_guru,
    create_nilai,
    update_nilai,
    delete_nilai,
)
from features.nilai.schemas import NilaiCreate, NilaiUpdate
from features.nilai.utils import validasi_nilai, hitung_nilai_akhir, tentukan_status
from core.exceptions import NotFoundException, BadRequestException, ForbiddenException


def list_nilai(db: Session, current_user: CurrentUser, kelas_id: int | None = None, mata_pelajaran_id: int | None = None) -> list[Nilai]:
    nis = None
    if current_user.role == "siswa":
        siswa = get_siswa_by_user_id(db, current_user.id)
        if siswa:
            nis = siswa.nis
        else:
            return []
    return get_nilai_filtered(db, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id, nis=nis)


def detail_nilai(db: Session, nilai_id: int) -> Nilai:
    nilai = get_nilai_by_id(db, nilai_id)
    if not nilai:
        raise NotFoundException("Nilai tidak ditemukan")
    return nilai


def create_new_nilai(db: Session, data: NilaiCreate, current_user: CurrentUser) -> Nilai:
    if not validasi_nilai(data.tugas):
        raise BadRequestException("Nilai tugas harus 0-100")
    if not validasi_nilai(data.uts):
        raise BadRequestException("Nilai UTS harus 0-100")
    if not validasi_nilai(data.uas):
        raise BadRequestException("Nilai UAS harus 0-100")
    siswa = get_siswa_by_nis(db, data.nis)
    if not siswa:
        raise BadRequestException("Siswa tidak ditemukan")
    if current_user.role == "guru":
        if not current_user.guru:
            raise ForbiddenException("Akun guru tidak valid")
        gm = get_guru_mengajar_by_id_and_guru(db, data.guru_mengajar_id, current_user.guru.id)
    else:
        gm = get_guru_mengajar_by_id(db, data.guru_mengajar_id)
    if not gm:
        raise BadRequestException("Data guru mengajar tidak ditemukan")
    nilai = Nilai(
        nis=data.nis,
        guru_mengajar_id=data.guru_mengajar_id,
        tugas=data.tugas,
        uts=data.uts,
        uas=data.uas,
        nilai_akhir=hitung_nilai_akhir(data.tugas, data.uts, data.uas),
        status=tentukan_status(hitung_nilai_akhir(data.tugas, data.uts, data.uas)),
    )
    return create_nilai(db, nilai)


def update_existing_nilai(db: Session, nilai_id: int, data: NilaiUpdate, current_user: CurrentUser) -> Nilai:
    nilai = get_nilai_by_id(db, nilai_id)
    if not nilai:
        raise NotFoundException("Nilai tidak ditemukan")
    if current_user.role == "guru":
        if not current_user.guru or nilai.guru_mengajar.guru_id != current_user.guru.id:
            raise ForbiddenException("Anda tidak berhak mengubah nilai ini")
    if data.tugas is not None:
        if not validasi_nilai(data.tugas):
            raise BadRequestException("Nilai tugas harus 0-100")
        nilai.tugas = data.tugas
    if data.uts is not None:
        if not validasi_nilai(data.uts):
            raise BadRequestException("Nilai UTS harus 0-100")
        nilai.uts = data.uts
    if data.uas is not None:
        if not validasi_nilai(data.uas):
            raise BadRequestException("Nilai UAS harus 0-100")
        nilai.uas = data.uas
    nilai.nilai_akhir = hitung_nilai_akhir(nilai.tugas, nilai.uts, nilai.uas)
    nilai.status = tentukan_status(nilai.nilai_akhir)
    return update_nilai(db, nilai)


def list_nilai_by_siswa_service(db: Session, nis: str, current_user: CurrentUser) -> list[Nilai]:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise NotFoundException("Siswa tidak ditemukan")
    if current_user.role == "siswa":
        current_siswa = get_siswa_by_user_id(db, current_user.id)
        if not current_siswa or current_siswa.nis != nis:
            raise ForbiddenException("Access denied")
    return get_nilai_by_siswa(db, nis)


def delete_existing_nilai(db: Session, nilai_id: int, current_user: CurrentUser) -> None:
    nilai = get_nilai_by_id(db, nilai_id)
    if not nilai:
        raise NotFoundException("Nilai tidak ditemukan")
    delete_nilai(db, nilai)
