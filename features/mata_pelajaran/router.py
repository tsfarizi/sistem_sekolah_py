from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user, require_admin, CurrentUser
from core.schemas import Message
from features.mata_pelajaran.schemas import MataPelajaranCreate, MataPelajaranUpdate, MataPelajaranResponse
from features.mata_pelajaran.service import list_matapelajaran, detail_matapelajaran, create_matapelajaran, update_matapelajaran, delete_matapelajaran

router = APIRouter(prefix="/api/mata-pelajaran", tags=["Mata Pelajaran"])


@router.get("", response_model=list[MataPelajaranResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return list_matapelajaran(db)


@router.get("/{id}", response_model=MataPelajaranResponse)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return detail_matapelajaran(db, id)


@router.post("", response_model=MataPelajaranResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: MataPelajaranCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    return create_matapelajaran(db, data)


@router.put("/{id}", response_model=MataPelajaranResponse)
def update(
    id: int,
    data: MataPelajaranUpdate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    return update_matapelajaran(db, id, data)


@router.delete("/{id}", response_model=Message)
def delete(
    id: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    delete_matapelajaran(db, id)
    return {"message": "Mata pelajaran berhasil dihapus"}
