from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user, require_admin, CurrentUser
from core.schemas import Message
from features.guru_mengajar.schemas import GuruMengajarCreate, GuruMengajarResponse
from features.guru_mengajar.service import list_guru_mengajar, detail_guru_mengajar, create_guru_mengajar, delete_guru_mengajar

router = APIRouter(prefix="/api/guru-mengajar", tags=["Guru Mengajar"])


@router.get("", response_model=list[GuruMengajarResponse])
def get_all(
    guru_id: str | None = Query(None),
    kelas_id: int | None = Query(None),
    mata_pelajaran_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return list_guru_mengajar(db, guru_id=guru_id, kelas_id=kelas_id, mata_pelajaran_id=mata_pelajaran_id)


@router.get("/{id}", response_model=GuruMengajarResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return detail_guru_mengajar(db, id)


@router.post("", response_model=GuruMengajarResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: GuruMengajarCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    return create_guru_mengajar(db, data)


@router.delete("/{id}", response_model=Message)
def delete(
    id: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    delete_guru_mengajar(db, id)
    return {"message": "Data guru mengajar berhasil dihapus"}
