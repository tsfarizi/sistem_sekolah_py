from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.kelas.models import Kelas
from features.kelas.repository import get_all, get_by_id, create, update, delete
from features.kelas.schemas import KelasCreate, KelasUpdate
from features.guru.models import Guru


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
    if data.wali_kelas_id:
        guru = db.query(Guru).filter(Guru.id == data.wali_kelas_id).first()
        if not guru:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guru tidak ditemukan")
    kelas = Kelas(nama=data.nama, wali_kelas_id=data.wali_kelas_id)
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
    if data.wali_kelas_id is not None:
        if data.wali_kelas_id != "":
            guru = db.query(Guru).filter(Guru.id == data.wali_kelas_id).first()
            if not guru:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guru tidak ditemukan")
            kelas.wali_kelas_id = data.wali_kelas_id
        else:
            kelas.wali_kelas_id = None
    return update(db, kelas)


def delete_kelas(db: Session, kelas_id: int) -> None:
    kelas = get_by_id(db, kelas_id)
    if not kelas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kelas tidak ditemukan")
    delete(db, kelas)
