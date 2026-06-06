from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.kelas.models import Kelas
from features.kelas.repository import get_all, get_by_id, create, update, delete
from features.kelas.schemas import KelasCreate, KelasUpdate


def list_kelas(db: Session) -> list[Kelas]:
    return get_all(db)


def detail_kelas(db: Session, kelas_id: int) -> Kelas:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelas tidak ditemukan")
    return kelas


def create_kelas(db: Session, data: KelasCreate) -> Kelas:
    existing = db.query(Kelas).filter(Kelas.nama == data.nama).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kelas sudah ada")
    kelas = Kelas(nama=data.nama)
    return create(db, kelas)


def update_kelas(db: Session, kelas_id: int, data: KelasUpdate) -> Kelas:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelas tidak ditemukan")
    if data.nama is not None:
        existing = db.query(Kelas).filter(Kelas.nama == data.nama, Kelas.id != kelas_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kelas sudah ada")
        kelas.nama = data.nama
    return update(db, kelas)


def delete_kelas(db: Session, kelas_id: int) -> None:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelas tidak ditemukan")
    delete(db, kelas)
