from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from features.auth.models import User
from features.guru.schemas import GuruCreate, GuruUpdate, GuruResponse
from features.guru.service import (
    list_guru,
    detail_guru,
    create_new_guru,
    update_existing_guru,
    delete_existing_guru,
)

router = APIRouter(prefix="/api/guru", tags=["Guru"])


@router.get("", response_model=list[GuruResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_guru(db)


@router.get("/{id}", response_model=GuruResponse)
def get_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detail_guru(db, id)


@router.post("", response_model=GuruResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: GuruCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return create_new_guru(db, data)


@router.put("/{id}", response_model=GuruResponse)
def update(
    id: str,
    data: GuruUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return update_existing_guru(db, id, data)


@router.delete("/{id}")
def delete(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    delete_existing_guru(db, id)
    return {"message": "Guru berhasil dihapus"}
