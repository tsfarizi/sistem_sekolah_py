from sqlalchemy.orm import Session
from features.mata_pelajaran.models import MataPelajaran
from features.mata_pelajaran.repository import (
    get_all_matapelajaran as repo_get_all,
    get_matapelajaran_by_id as repo_get_by_id,
    get_by_nama,
    get_by_nama_excluding,
    create_matapelajaran as repo_create,
    update_matapelajaran as repo_update,
    delete_matapelajaran as repo_delete,
)
from features.mata_pelajaran.schemas import MataPelajaranCreate, MataPelajaranUpdate
from core.exceptions import NotFoundException, BadRequestException


def list_matapelajaran(db: Session) -> list[MataPelajaran]:
    return repo_get_all(db)


def detail_matapelajaran(db: Session, matapelajaran_id: int) -> MataPelajaran:
    matapelajaran = repo_get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    return matapelajaran


def create_matapelajaran(db: Session, data: MataPelajaranCreate) -> MataPelajaran:
    existing = get_by_nama(db, data.nama)
    if existing:
        raise BadRequestException("Mata pelajaran sudah ada")
    matapelajaran = MataPelajaran(nama=data.nama)
    return repo_create(db, matapelajaran)


def update_matapelajaran(db: Session, matapelajaran_id: int, data: MataPelajaranUpdate) -> MataPelajaran:
    matapelajaran = repo_get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    if data.nama is not None:
        existing = get_by_nama_excluding(db, data.nama, matapelajaran_id)
        if existing:
            raise BadRequestException("Mata pelajaran sudah ada")
        matapelajaran.nama = data.nama
    return repo_update(db, matapelajaran)


def delete_matapelajaran(db: Session, matapelajaran_id: int) -> None:
    matapelajaran = repo_get_by_id(db, matapelajaran_id)
    if not matapelajaran:
        raise NotFoundException("Mata pelajaran tidak ditemukan")
    repo_delete(db, matapelajaran)
