from sqlalchemy.orm import Session, joinedload
from features.guru_mengajar.models import GuruMengajar
from features.guru.models import Guru
from features.kelas.models import Kelas
from features.mata_pelajaran.models import MataPelajaran


def get_all(db: Session, guru_id: str | None = None, kelas_id: int | None = None, mata_pelajaran_id: int | None = None) -> list[GuruMengajar]:
    query = db.query(GuruMengajar).options(
        joinedload(GuruMengajar.guru),
        joinedload(GuruMengajar.kelas),
        joinedload(GuruMengajar.mata_pelajaran),
    )
    if guru_id:
        query = query.filter(GuruMengajar.guru_id == guru_id)
    if kelas_id:
        query = query.filter(GuruMengajar.kelas_id == kelas_id)
    if mata_pelajaran_id:
        query = query.filter(GuruMengajar.mata_pelajaran_id == mata_pelajaran_id)
    return query.all()


def get_by_id(db: Session, gm_id: int) -> GuruMengajar | None:
    return db.query(GuruMengajar).options(
        joinedload(GuruMengajar.guru),
        joinedload(GuruMengajar.kelas),
        joinedload(GuruMengajar.mata_pelajaran),
    ).filter(GuruMengajar.id == gm_id).first()


def get_by_combination(db: Session, guru_id: str, kelas_id: int, mata_pelajaran_id: int) -> GuruMengajar | None:
    return db.query(GuruMengajar).filter(
        GuruMengajar.guru_id == guru_id,
        GuruMengajar.kelas_id == kelas_id,
        GuruMengajar.mata_pelajaran_id == mata_pelajaran_id,
    ).first()


def get_guru_by_id(db: Session, guru_id: str) -> Guru | None:
    return db.query(Guru).filter(Guru.id == guru_id).first()


def get_kelas_by_id(db: Session, kelas_id: int) -> Kelas | None:
    return db.query(Kelas).filter(Kelas.id == kelas_id).first()


def get_matapelajaran_by_id(db: Session, matapelajaran_id: int) -> MataPelajaran | None:
    return db.query(MataPelajaran).filter(MataPelajaran.id == matapelajaran_id).first()


def create(db: Session, gm: GuruMengajar) -> GuruMengajar:
    db.add(gm)
    db.commit()
    db.refresh(gm)
    return gm


def create_and_eager_load(db: Session, gm: GuruMengajar) -> GuruMengajar:
    db.add(gm)
    db.commit()
    result = db.query(GuruMengajar).options(
        joinedload(GuruMengajar.guru),
        joinedload(GuruMengajar.kelas),
        joinedload(GuruMengajar.mata_pelajaran),
    ).filter(GuruMengajar.id == gm.id).first()
    assert result is not None
    return result


def delete(db: Session, gm: GuruMengajar) -> None:
    db.delete(gm)
    db.commit()
