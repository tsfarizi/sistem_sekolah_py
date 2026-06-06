from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.guru.models import Guru
from features.guru.repository import (
    get_all_guru,
    get_guru_by_id,
    create_guru as repo_create_guru,
    update_guru as repo_update_guru,
    delete_guru as repo_delete_guru,
)
from features.guru.schemas import GuruCreate, GuruUpdate
from features.auth.models import User
from core.security import hash_password


def list_guru(db: Session) -> list[Guru]:
    return get_all_guru(db)


def detail_guru(db: Session, guru_id: str) -> Guru:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guru tidak ditemukan"
        )
    return guru


def create_new_guru(db: Session, data: GuruCreate) -> Guru:
    existing = get_guru_by_id(db, data.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID Guru sudah digunakan"
        )
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah digunakan"
        )
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role="guru",
        nama=data.nama,
    )
    db.add(user)
    db.flush()
    guru = Guru(
        id=data.id,
        nama=data.nama,
        user_id=user.id,
    )
    return repo_create_guru(db, guru)


def update_existing_guru(db: Session, guru_id: str, data: GuruUpdate) -> Guru:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guru tidak ditemukan"
        )
    if data.nama is not None:
        guru.nama = data.nama
        if guru.user:
            guru.user.nama = data.nama
    return repo_update_guru(db, guru)


def delete_existing_guru(db: Session, guru_id: str) -> None:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guru tidak ditemukan"
        )
    user_id = guru.user_id
    db.delete(guru)
    db.flush()
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()
