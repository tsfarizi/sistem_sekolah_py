from sqlalchemy.orm import Session
from features.guru.models import Guru
from features.auth.models import User
from core.security import hash_password


def get_all_guru(db: Session) -> list[Guru]:
    return db.query(Guru).all()


def get_guru_by_id(db: Session, guru_id: str) -> Guru | None:
    return db.query(Guru).filter(Guru.id == guru_id).first()


def get_last_guru(db: Session) -> Guru | None:
    return db.query(Guru).order_by(Guru.id.desc()).first()


def create_guru(db: Session, guru: Guru) -> Guru:
    db.add(guru)
    db.commit()
    db.refresh(guru)
    return guru


def create_guru_with_user(db: Session, guru: Guru, username: str, password: str, nama: str) -> Guru:
    user = User(
        username=username,
        password_hash=hash_password(password),
        role="guru",
        nama=nama,
    )
    db.add(user)
    db.flush()
    guru.user_id = user.id
    db.add(guru)
    db.commit()
    db.refresh(guru)
    return guru


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_guru(db: Session, guru: Guru) -> Guru:
    db.commit()
    db.refresh(guru)
    return guru


def delete_guru_and_user(db: Session, guru: Guru) -> None:
    user_id = guru.user_id
    db.delete(guru)
    db.flush()
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()


def delete_guru(db: Session, guru: Guru) -> None:
    db.delete(guru)
    db.commit()
