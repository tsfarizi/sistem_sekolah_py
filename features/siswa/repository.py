from sqlalchemy.orm import Session, joinedload
from features.siswa.models import Siswa
from features.nilai.models import Nilai
from features.guru_mengajar.models import GuruMengajar


def get_all_siswa(db: Session) -> list[Siswa]:
    return db.query(Siswa).all()


def get_siswa_by_nis(db: Session, nis: str) -> Siswa | None:
    return db.query(Siswa).options(
        joinedload(Siswa.kelas),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.guru),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.kelas),
        joinedload(Siswa.nilai_list).joinedload(Nilai.guru_mengajar).joinedload(GuruMengajar.mata_pelajaran),
        joinedload(Siswa.nilai_list).joinedload(Nilai.siswa),
    ).filter(Siswa.nis == nis).first()


def create_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa


def update_siswa(db: Session, siswa: Siswa) -> Siswa:
    db.commit()
    db.refresh(siswa)
    return siswa


def delete_siswa(db: Session, siswa: Siswa) -> None:
    db.delete(siswa)
    db.commit()
