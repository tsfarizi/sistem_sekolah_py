from sqlalchemy.orm import Session
from features.nilai.models import Nilai
from features.siswa.models import Siswa
from features.guru_mengajar.models import GuruMengajar


def get_all_nilai(db: Session) -> list[Nilai]:
    return db.query(Nilai).all()


def get_nilai_by_id(db: Session, nilai_id: int) -> Nilai | None:
    return db.query(Nilai).filter(Nilai.id == nilai_id).first()


def get_nilai_by_siswa(db: Session, nis: str) -> list[Nilai]:
    return db.query(Nilai).filter(Nilai.nis == nis).all()


def get_nilai_filtered(db: Session, kelas_id: int | None = None, mata_pelajaran_id: int | None = None, nis: str | None = None) -> list[Nilai]:
    query = db.query(Nilai)
    if nis:
        query = query.filter(Nilai.nis == nis)
    if kelas_id or mata_pelajaran_id:
        query = query.join(Nilai.guru_mengajar)
        if kelas_id:
            query = query.filter(GuruMengajar.kelas_id == kelas_id)
        if mata_pelajaran_id:
            query = query.filter(GuruMengajar.mata_pelajaran_id == mata_pelajaran_id)
    return query.all()


def get_siswa_by_nis(db: Session, nis: str) -> Siswa | None:
    return db.query(Siswa).filter(Siswa.nis == nis).first()


def get_siswa_by_user_id(db: Session, user_id: int) -> Siswa | None:
    return db.query(Siswa).filter(Siswa.user_id == user_id).first()


def get_guru_mengajar_by_id(db: Session, gm_id: int) -> GuruMengajar | None:
    return db.query(GuruMengajar).filter(GuruMengajar.id == gm_id).first()


def get_guru_mengajar_by_id_and_guru(db: Session, gm_id: int, guru_id: str) -> GuruMengajar | None:
    return db.query(GuruMengajar).filter(
        GuruMengajar.id == gm_id,
        GuruMengajar.guru_id == guru_id,
    ).first()


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
