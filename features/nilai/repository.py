from sqlalchemy.orm import Session
from features.nilai.models import Nilai


def get_all_nilai(db: Session) -> list[Nilai]:
    return db.query(Nilai).all()


def get_nilai_by_id(db: Session, nilai_id: int) -> Nilai | None:
    return db.query(Nilai).filter(Nilai.id == nilai_id).first()


def get_nilai_by_siswa(db: Session, nis: str) -> list[Nilai]:
    return db.query(Nilai).filter(Nilai.nis == nis).all()


def create_nilai(db: Session, nilai: Nilai) -> Nilai:
    db.add(nilai)
    db.commit()
    db.refresh(nilai)
    return nilai


def update_nilai(db: Session, nilai: Nilai) -> Nilai:
    db.commit()
    db.refresh(nilai)
    return nilai


def delete_nilai(db: Session, nilai: Nilai) -> None:
    db.delete(nilai)
    db.commit()
