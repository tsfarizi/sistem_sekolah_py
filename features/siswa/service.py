from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.siswa.models import Siswa
from features.siswa.repository import (
    get_all_siswa,
    get_siswa_by_nis,
    create_siswa as repo_create_siswa,
    update_siswa as repo_update_siswa,
    delete_siswa as repo_delete_siswa,
)
from features.siswa.schemas import SiswaCreate, SiswaUpdate
from features.auth.models import User
from features.kelas.models import Kelas
from core.security import hash_password


def list_siswa(db: Session, kelas_id: int | None = None) -> list[Siswa]:
    if kelas_id:
        return db.query(Siswa).filter(Siswa.kelas_id == kelas_id).all()
    return get_all_siswa(db)


def detail_siswa(db: Session, nis: str) -> Siswa:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Siswa tidak ditemukan"
        )
    return siswa


def create_new_siswa(db: Session, data: SiswaCreate) -> Siswa:
    existing = get_siswa_by_nis(db, data.nis)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="NIS sudah digunakan"
        )
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah digunakan"
        )
    kelas = db.query(Kelas).filter(Kelas.id == data.kelas_id).first()
    if not kelas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Kelas tidak ditemukan"
        )
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role="siswa",
        nama=data.nama,
    )
    db.add(user)
    db.flush()
    siswa = Siswa(
        nis=data.nis,
        nama=data.nama,
        kelas_id=data.kelas_id,
        user_id=user.id,
    )
    return repo_create_siswa(db, siswa)


def update_existing_siswa(db: Session, nis: str, data: SiswaUpdate) -> Siswa:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Siswa tidak ditemukan"
        )
    if data.nama is not None:
        siswa.nama = data.nama
        if siswa.user:
            siswa.user.nama = data.nama
    if data.kelas_id is not None:
        kelas = db.query(Kelas).filter(Kelas.id == data.kelas_id).first()
        if not kelas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Kelas tidak ditemukan"
            )
        siswa.kelas_id = data.kelas_id
    return repo_update_siswa(db, siswa)


def delete_existing_siswa(db: Session, nis: str) -> None:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Siswa tidak ditemukan"
        )
    user_id = siswa.user_id
    db.delete(siswa)
    db.flush()
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()
