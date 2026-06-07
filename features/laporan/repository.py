from sqlalchemy.orm import Session
from features.nilai.models import Nilai
from features.siswa.models import Siswa
from features.guru_mengajar.models import GuruMengajar
from features.nilai.utils import nilai_to_dict


def get_nilai_joined(db: Session, kelas_id: int | None = None, kelas_ids: list[int] | None = None) -> list[Nilai]:
    query = db.query(Nilai).join(Nilai.guru_mengajar)
    if kelas_id:
        query = query.filter(GuruMengajar.kelas_id == kelas_id)
    if kelas_ids:
        query = query.filter(GuruMengajar.kelas_id.in_(kelas_ids))
    return query.all()


def get_nilai_by_nis(db: Session, nis: str) -> list[Nilai]:
    return db.query(Nilai).filter(Nilai.nis == nis).all()


def get_siswa_by_nis(db: Session, nis: str) -> Siswa | None:
    return db.query(Siswa).filter(Siswa.nis == nis).first()


def get_kelas_ids_by_guru(db: Session, guru_id: str) -> list[int]:
    rows = db.query(GuruMengajar.kelas_id).filter(GuruMengajar.guru_id == guru_id).distinct().all()
    return [r[0] for r in rows]


def nilai_list_to_dicts(nilai_list: list[Nilai]) -> list[dict]:
    return [nilai_to_dict(n) for n in nilai_list]
