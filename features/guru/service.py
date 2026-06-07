from sqlalchemy.orm import Session
from features.guru.models import Guru
from features.guru.repository import (
    get_all_guru,
    get_guru_by_id,
    get_last_guru,
    get_user_by_username,
    create_guru_with_user,
    update_guru,
    delete_guru_and_user,
)
from features.guru.schemas import GuruCreate, GuruUpdate
from core.exceptions import NotFoundException, BadRequestException


def _generate_guru_id(db: Session) -> str:
    last = get_last_guru(db)
    if not last:
        return "G001"
    try:
        num = int(last.id[1:]) + 1
        return f"G{num:03d}"
    except (ValueError, IndexError):
        return "G001"


def list_guru(db: Session) -> list[Guru]:
    return get_all_guru(db)


def detail_guru(db: Session, guru_id: str) -> Guru:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise NotFoundException("Guru tidak ditemukan")
    return guru


def create_new_guru(db: Session, data: GuruCreate) -> Guru:
    guru_id = data.id if data.id else _generate_guru_id(db)
    existing = get_guru_by_id(db, guru_id)
    if existing:
        raise BadRequestException("ID Guru sudah digunakan")
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise BadRequestException("Username sudah digunakan")
    guru = Guru(id=guru_id, nama=data.nama)
    return create_guru_with_user(db, guru, data.username, data.password, data.nama)


def update_existing_guru(db: Session, guru_id: str, data: GuruUpdate) -> Guru:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise NotFoundException("Guru tidak ditemukan")
    if data.nama is not None:
        guru.nama = data.nama
        if guru.user:
            guru.user.nama = data.nama
    return update_guru(db, guru)


def delete_existing_guru(db: Session, guru_id: str) -> None:
    guru = get_guru_by_id(db, guru_id)
    if not guru:
        raise NotFoundException("Guru tidak ditemukan")
    delete_guru_and_user(db, guru)
