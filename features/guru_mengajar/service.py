from sqlalchemy.orm import Session
from features.guru_mengajar.models import GuruMengajar
from features.guru_mengajar.repository import (
    get_all as repo_get_all,
    get_by_id,
    get_by_combination,
    get_guru_by_id,
    get_kelas_by_id,
    get_matapelajaran_by_id,
    create_and_eager_load,
    delete as repo_delete,
)
from features.guru_mengajar.schemas import GuruMengajarCreate
from core.exceptions import NotFoundException, BadRequestException


def list_guru_mengajar(db: Session, guru_id: str | None = None, kelas_id: int | None = None, mata_pelajaran_id: int | None = None) -> list[GuruMengajar]:
    return repo_get_all(db, guru_id=guru_id, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id)


def detail_guru_mengajar(db: Session, gm_id: int) -> GuruMengajar:
    gm = get_by_id(db, gm_id)
    if not gm:
        raise NotFoundException("Data tidak ditemukan")
    return gm


def create_guru_mengajar(db: Session, data: GuruMengajarCreate) -> GuruMengajar:
    guru = get_guru_by_id(db, data.guru_id)
    if not guru:
        raise BadRequestException("Guru tidak ditemukan")
    kelas = get_kelas_by_id(db, data.kelas_id)
    if not kelas:
        raise BadRequestException("Kelas tidak ditemukan")
    matapelajaran = get_matapelajaran_by_id(db, data.mata_pelajaran_id)
    if not matapelajaran:
        raise BadRequestException("Mata pelajaran tidak ditemukan")
    existing = get_by_combination(db, data.guru_id, data.kelas_id, data.mata_pelajaran_id)
    if existing:
        raise BadRequestException("Kombinasi guru-kelas-mata pelajaran sudah ada")
    gm = GuruMengajar(
        guru_id=data.guru_id,
        kelas_id=data.kelas_id,
        mata_pelajaran_id=data.mata_pelajaran_id,
    )
    return create_and_eager_load(db, gm)


def delete_guru_mengajar(db: Session, gm_id: int) -> None:
    gm = get_by_id(db, gm_id)
    if not gm:
        raise NotFoundException("Data tidak ditemukan")
    repo_delete(db, gm)
