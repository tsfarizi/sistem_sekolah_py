from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from features.guru_mengajar.models import GuruMengajar
from features.guru_mengajar.repository import get_all as repo_get_all, get_by_id, create as repo_create, delete as repo_delete
from features.guru_mengajar.schemas import GuruMengajarCreate
from features.guru.models import Guru
from features.kelas.models import Kelas
from features.mata_pelajaran.models import MataPelajaran


def list_guru_mengajar(db: Session, guru_id: str | None = None, kelas_id: int | None = None, mata_pelajaran_id: int | None = None) -> list[GuruMengajar]:
    return repo_get_all(db, guru_id=guru_id, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id)


def detail_guru_mengajar(db: Session, gm_id: int) -> GuruMengajar:
    gm = get_by_id(db, gm_id)
    if not gm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")
    return gm


def create_guru_mengajar(db: Session, data: GuruMengajarCreate) -> GuruMengajar:
    guru = db.query(Guru).filter(Guru.id == data.guru_id).first()
    if not guru:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guru tidak ditemukan")
    kelas = db.query(Kelas).filter(Kelas.id == data.kelas_id).first()
    if not kelas:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kelas tidak ditemukan")
    mapel = db.query(MataPelajaran).filter(MataPelajaran.id == data.mata_pelajaran_id).first()
    if not mapel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mata pelajaran tidak ditemukan")

    existing = db.query(GuruMengajar).filter(
        GuruMengajar.guru_id == data.guru_id,
        GuruMengajar.kelas_id == data.kelas_id,
        GuruMengajar.mata_pelajaran_id == data.mata_pelajaran_id,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kombinasi guru-kelas-mapel sudah ada")

    gm = GuruMengajar(
        guru_id=data.guru_id,
        kelas_id=data.kelas_id,
        mata_pelajaran_id=data.mata_pelajaran_id,
    )
    gm = repo_create(db, gm)
    return db.query(GuruMengajar).options(
        joinedload(GuruMengajar.guru),
        joinedload(GuruMengajar.kelas),
        joinedload(GuruMengajar.mata_pelajaran),
    ).filter(GuruMengajar.id == gm.id).first()


def delete_guru_mengajar(db: Session, gm_id: int) -> None:
    gm = get_by_id(db, gm_id)
    if not gm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")
    repo_delete(db, gm)
