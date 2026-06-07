from sqlalchemy.orm import Session
from features.kelas.models import Kelas


def get_all_kelas(db: Session) -> list[Kelas]:
    return db.query(Kelas).all()


def get_kelas_by_id(db: Session, kelas_id: int) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.id == kelas_id).first()


def get_by_nama(db: Session, nama: str) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.nama == nama).first()


def get_by_nama_excluding(db: Session, nama: str, exclude_id: int) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.nama == nama, Kelas.id != exclude_id).first()


def create_kelas(db: Session, kelas: Kelas) -> Kelas:
    db.add(kelas)
    db.commit()
    db.refresh(kelas)
    return kelas


def update_kelas(db: Session, kelas: Kelas) -> Kelas:
    db.commit()
    db.refresh(kelas)
    return kelas


def delete_kelas(db: Session, kelas: Kelas) -> None:
    db.delete(kelas)
    db.commit()
