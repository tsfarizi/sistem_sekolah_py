from datetime import datetime
from sqlalchemy.orm import Session
from features.siswa.models import Siswa
from features.siswa.repository import (
    get_all_siswa,
    get_siswa_by_kelas,
    get_siswa_by_nis,
    get_last_siswa_by_year,
    get_user_by_username,
    get_kelas_by_id,
    create_siswa_with_user,
    update_siswa,
    delete_siswa_and_user,
)
from features.siswa.schemas import SiswaCreate, SiswaUpdate
from core.exceptions import NotFoundException, BadRequestException


def _generate_nis(db: Session) -> str:
    year = str(datetime.utcnow().year)
    last = get_last_siswa_by_year(db, year)
    if not last:
        return f"{year}0001"
    try:
        num = int(last.nis[4:]) + 1
        return f"{year}{num:04d}"
    except (ValueError, IndexError):
        return f"{year}0001"


def list_siswa(db: Session, kelas_id: int | None = None) -> list[Siswa]:
    if kelas_id:
        return get_siswa_by_kelas(db, kelas_id)
    return get_all_siswa(db)


def detail_siswa(db: Session, nis: str) -> Siswa:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise NotFoundException("Siswa tidak ditemukan")
    return siswa


def create_new_siswa(db: Session, data: SiswaCreate) -> Siswa:
    nis = data.nis if data.nis else _generate_nis(db)
    existing = get_siswa_by_nis(db, nis)
    if existing:
        raise BadRequestException("NIS sudah digunakan")
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise BadRequestException("Username sudah digunakan")
    kelas = get_kelas_by_id(db, data.kelas_id)
    if not kelas:
        raise BadRequestException("Kelas tidak ditemukan")
    siswa = Siswa(nis=nis, nama=data.nama, kelas_id=data.kelas_id)
    return create_siswa_with_user(db, siswa, data.username, data.password, data.nama)


def update_existing_siswa(db: Session, nis: str, data: SiswaUpdate) -> Siswa:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise NotFoundException("Siswa tidak ditemukan")
    if data.nama is not None:
        siswa.nama = data.nama
        if siswa.user:
            siswa.user.nama = data.nama
    if data.kelas_id is not None:
        kelas = get_kelas_by_id(db, data.kelas_id)
        if not kelas:
            raise BadRequestException("Kelas tidak ditemukan")
        siswa.kelas_id = data.kelas_id
    return update_siswa(db, siswa)


def delete_existing_siswa(db: Session, nis: str) -> None:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise NotFoundException("Siswa tidak ditemukan")
    delete_siswa_and_user(db, siswa)
