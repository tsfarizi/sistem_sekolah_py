from sqlalchemy.orm import Session
from features.mata_pelajaran.models import MataPelajaran


def get_all_matapelajaran(db: Session) -> list[MataPelajaran]:
    return db.query(MataPelajaran).all()


def get_matapelajaran_by_id(db: Session, matapelajaran_id: int) -> MataPelajaran | None:
    return db.query(MataPelajaran).filter(MataPelajaran.id == matapelajaran_id).first()


def get_by_nama(db: Session, nama: str) -> MataPelajaran | None:
    return db.query(MataPelajaran).filter(MataPelajaran.nama == nama).first()


def get_by_nama_excluding(db: Session, nama: str, exclude_id: int) -> MataPelajaran | None:
    return db.query(MataPelajaran).filter(MataPelajaran.nama == nama, MataPelajaran.id != exclude_id).first()


def create_matapelajaran(db: Session, matapelajaran: MataPelajaran) -> MataPelajaran:
    db.add(matapelajaran)
    db.commit()
    db.refresh(matapelajaran)
    return matapelajaran


def update_matapelajaran(db: Session, matapelajaran: MataPelajaran) -> MataPelajaran:
    db.commit()
    db.refresh(matapelajaran)
    return matapelajaran


def delete_matapelajaran(db: Session, matapelajaran: MataPelajaran) -> None:
    db.delete(matapelajaran)
    db.commit()
