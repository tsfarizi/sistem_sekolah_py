from sqlalchemy.orm import Session
from features.kelas.models import Kelas


def get_all(db: Session) -> list[Kelas]:
    return db.query(Kelas).all()


def get_by_id(db: Session, kelas_id: int) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.id == kelas_id).first()


def create(db: Session, kelas: Kelas) -> Kelas:
    db.add(kelas)
    db.commit()
    db.refresh(kelas)
    return kelas


def update(db: Session, kelas: Kelas) -> Kelas:
    db.commit()
    db.refresh(kelas)
    return kelas


def delete(db: Session, kelas: Kelas) -> None:
    db.delete(kelas)
    db.commit()
