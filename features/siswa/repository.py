from sqlalchemy.orm import Session
from features.siswa.models import Siswa


def get_all_siswa(db: Session) -> list[Siswa]:
    return db.query(Siswa).all()


def get_siswa_by_nis(db: Session, nis: str) -> Siswa | None:
    return db.query(Siswa).filter(Siswa.nis == nis).first()


def create_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa


def update_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.commit()
    db.refresh(siswa)
    return siswa


def delete_siswa(db: Session, siswa: Siswa) -> None:
    db.delete(siswa)
    db.commit()
