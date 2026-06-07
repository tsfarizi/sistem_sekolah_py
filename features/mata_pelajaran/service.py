from sqlalchemy.orm import Session
from features.mata_pelajaran.models import MataPelajaran
from features.mata_pelajaran.repository import get_all, get_by_id, get_by_nama, get_by_nama_excluding, create, update, delete
from features.mata_pelajaran.schemas import MataPelajaranCreate, MataPelajaranUpdate
from core.exceptions import NotFoundException, BadRequestException


def list_matapelajaran(db: Session) -> list[MataPelajaran]:
    return get_all(db)


def detail_matapelajaran(db: Session, matapelajaran_id: int) -> MataPelajaran:
    matapelajaran = get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    return matapelajaran


def create_matapelajaran(db: Session, data: MataPelajaranCreate) -> MataPelajaran:
    existing = get_by_nama(db, data.nama)
    if existing:
        raise BadRequestException("Mata pelajaran sudah ada")
    matapelajaran = MataPelajaran(nama=data.nama)
    return create(db, matapelajaran)


def update_matapelajaran(db: Session, matapelajaran_id: int, data: MataPelajaranUpdate) -> MataPelajaran:
    matapelajaran = get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    if data.nama is not None:
        existing = get_by_nama_excluding(db, data.nama, matapelajaran_id)
        if existing:
            raise BadRequestException("Mata pelajaran sudah ada")
        matapelajaran.nama = data.nama
    return update(db, matapelajaran)


def delete_matapelajaran(db: Session, matapelajaran_id: int) -> None:
    matapelajaran = get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    delete(db, matapelajaran)
