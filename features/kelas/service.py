from sqlalchemy.orm import Session
from features.kelas.models import Kelas
from features.kelas.repository import (
    get_all_kelas as repo_get_all,
    get_kelas_by_id as repo_get_by_id,
    get_by_nama,
    get_by_nama_excluding,
    create_kelas as repo_create,
    update_kelas as repo_update,
    delete_kelas as repo_delete,
)
from features.kelas.schemas import KelasCreate, KelasUpdate
from core.exceptions import NotFoundException, BadRequestException


def list_kelas(db: Session) -> list[Kelas]:
    return repo_get_all(db)


def detail_kelas(db: Session, kelas_id: int) -> Kelas:
    kelas = repo_get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    return kelas


def create_kelas(db: Session, data: KelasCreate) -> Kelas:
    existing = get_by_nama(db, data.nama)
    if existing:
        raise BadRequestException("Kelas sudah ada")
    kelas = Kelas(nama=data.nama)
    return repo_create(db, kelas)


def update_kelas(db: Session, kelas_id: int, data: KelasUpdate) -> Kelas:
    kelas = repo_get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    if data.nama is not None:
        existing = get_by_nama_excluding(db, data.nama, kelas_id)
        if existing:
            raise BadRequestException("Kelas sudah ada")
        kelas.nama = data.nama
    return repo_update(db, kelas)


def delete_kelas(db: Session, kelas_id: int) -> None:
    kelas = repo_get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    repo_delete(db, kelas)
