from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from core.schemas import GuruMengajarRef, SiswaRef


class NilaiCreate(BaseModel):
    nis: str
    guru_mengajar_id: int
    tugas: float
    uts: float
    uas: float


class NilaiUpdate(BaseModel):
    tugas: Optional[float] = None
    uts: Optional[float] = None
    uas: Optional[float] = None


class NilaiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nis: str
    siswa: Optional[SiswaRef] = None
    guru_mengajar_id: int
    guru_mengajar: Optional[GuruMengajarRef] = None
    tugas: float
    uts: float
    uas: float
    nilai_akhir: float
    status: str
    created_at: datetime
    updated_at: datetime
