from sqlalchemy.orm import Session
from features.guru.models import Guru


def get_all_guru(db: Session) -> list[Guru]:
    return db.query(Guru).all()


def get_guru_by_id(db: Session, guru_id: str) -> Guru | None:
    return db.query(Guru).filter(Guru.id == guru_id).first()


def create_guru(db: Session, guru: Guru) -> Guru:
    db.add(guru)
    db.commit()
    db.refresh(guru)
    return guru


def update_guru(db: Session, guru: Guru) -> Guru:
    db.commit()
    db.refresh(guru)
    return guru


def delete_guru(db: Session, guru: Guru) -> None:
    db.delete(guru)
    db.commit()
