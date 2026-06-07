from sqlalchemy.orm import Session
from features.kelas.models import Kelas
from features.kelas.repository import get_all, get_by_id, get_by_nama, get_by_nama_excluding, create, update, delete
from features.kelas.schemas import KelasCreate, KelasUpdate
from core.exceptions import NotFoundException, BadRequestException


def list_kelas(db: Session) -> list[Kelas]:
    return get_all(db)


def detail_kelas(db: Session, kelas_id: int) -> Kelas:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    return kelas


def create_kelas(db: Session, data: KelasCreate) -> Kelas:
    existing = get_by_nama(db, data.nama)
    if existing:
        raise BadRequestException("Kelas sudah ada")
    kelas = Kelas(nama=data.nama)
    return create(db, kelas)


def update_kelas(db: Session, kelas_id: int, data: KelasUpdate) -> Kelas:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    if data.nama is not None:
        existing = get_by_nama_excluding(db, data.nama, kelas_id)
        if existing:
            raise BadRequestException("Kelas sudah ada")
        kelas.nama = data.nama
    return update(db, kelas)


def delete_kelas(db: Session, kelas_id: int) -> None:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise NotFoundException("Kelas tidak ditemukan")
    delete(db, kelas)
