from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.mata_pelajaran.models import MataPelajaran
from features.mata_pelajaran.repository import get_all, get_by_id, create, update, delete
from features.mata_pelajaran.schemas import MataPelajaranCreate, MataPelajaranUpdate


def list_mapel(db: Session) -> list[MataPelajaran]:
    return get_all(db)


def detail_mapel(db: Session, mapel_id: int) -> MataPelajaran:
    mapel = get_by_id(db, mapel_id)
    if not mapel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mata pelajaran tidak ditemukan")
    return mapel


def create_mapel(db: Session, data: MataPelajaranCreate) -> MataPelajaran:
    existing = db.query(MataPelajaran).filter(MataPelajaran.nama == data.nama).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mata pelajaran sudah ada")
    mapel = MataPelajaran(nama=data.nama)
    return create(db, mapel)


def update_mapel(db: Session, mapel_id: int, data: MataPelajaranUpdate) -> MataPelajaran:
    mapel = get_by_id(db, mapel_id)
    if not mapel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mata pelajaran tidak ditemukan")
    if data.nama is not None:
        existing = db.query(MataPelajaran).filter(MataPelajaran.nama == data.nama, MataPelajaran.id != mapel_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mata pelajaran sudah ada")
        mapel.nama = data.nama
    return update(db, mapel)


def delete_mapel(db: Session, mapel_id: int) -> None:
    mapel = get_by_id(db, mapel_id)
    if not mapel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mata pelajaran tidak ditemukan")
    delete(db, mapel)
