from sqlalchemy.orm import Session
from features.mata_pelajaran.models import MataPelajaran


def get_all(db: Session) -> list[MataPelajaran]:
    return db.query(MataPelajaran).all()


def get_by_id(db: Session, mapel_id: int) -> MataPelajaran | None:
    return db.query(MataPelajaran).filter(MataPelajaran.id == mapel_id).first()


def create(db: Session, mapel: MataPelajaran) -> MataPelajaran:
    db.add(mapel)
    db.commit()
    db.refresh(mapel)
    return mapel


def update(db: Session, mapel: MataPelajaran) -> MataPelajaran:
    db.commit()
    db.refresh(mapel)
    return mapel


def delete(db: Session, mapel: MataPelajaran) -> None:
    db.delete(mapel)
    db.commit()
