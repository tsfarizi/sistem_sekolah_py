from sqlalchemy.orm import Session, joinedload
from features.siswa.models import Siswa
from features.auth.models import User
from features.kelas.models import Kelas
from features.nilai.models import Nilai
from features.guru_mengajar.models import GuruMengajar
from core.security import hash_password


def get_all_siswa(db: Session) -> list[Siswa]:
    return db.query(Siswa).all()


def get_siswa_by_kelas(db: Session, kelas_id: int) -> list[Siswa]:
    return db.query(Siswa).filter(Siswa.kelas_id == kelas_id).all()


def get_siswa_by_nis(db: Session, nis: str) -> Siswa | None:
    return db.query(Siswa).options(
        joinedload(Siswa.kelas),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.guru),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.kelas),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.mata_pelajaran),
        joinedload(Siswa.nilai_list).joinedload(Nilai.siswa),
    ).filter(Siswa.nis == nis).first()


def get_last_siswa_by_year(db: Session, year: str) -> Siswa | None:
    return db.query(Siswa).filter(Siswa.nis.like(f"{year}%")).order_by(Siswa.nis.desc()).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_kelas_by_id(db: Session, kelas_id: int) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.id == kelas_id).first()


def create_siswa_with_user(db: Session, siswa: Siswa, username: str, password: str, nama: str) -> Siswa:
    user = User(
        username=username,
        password_hash=hash_password(password),
        role="siswa",
        nama=nama,
    )
    db.add(user)
    db.flush()
    siswa.user_id = user.id
    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa


def create_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa


def update_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.commit()
    db.refresh(siswa)
    return siswa


def delete_siswa_and_user(db: Session, siswa: Siswa) -> None:
    user_id = siswa.user_id
    db.delete(siswa)
    db.flush()
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()


def delete_siswa(db: Session, siswa: Siswa) -> None:
    db.delete(siswa)
    db.commit()
