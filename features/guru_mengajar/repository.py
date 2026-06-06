from sqlalchemy.orm import Session, joinedload
from features.guru_mengajar.models import GuruMengajar


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


def create(db: Session, gm: GuruMengajar) -> GuruMengajar:
    db.add(gm)
    db.commit()
    db.refresh(gm)
    return gm


def delete(db: Session, gm: GuruMengajar) -> None:
    db.delete(gm)
    db.commit()
