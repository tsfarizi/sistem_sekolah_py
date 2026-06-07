from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from core.schemas import GuruMengajarRef, SiswaRef


class NilaiCreate(BaseModel):
    nis: str
    guru_mengajar_id: int
    tugas: float = Field(ge=0, le=100)
    uts: float = Field(ge=0, le=100)
    uas: float = Field(ge=0, le=100)


class NilaiUpdate(BaseModel):
    tugas: float | None = Field(default=None, ge=0, le=100)
    uts: float | None = Field(default=None, ge=0, le=100)
    uas: float | None = Field(default=None, ge=0, le=100)


class NilaiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nis: str
    siswa: SiswaRef | None = None
    guru_mengajar_id: int
    guru_mengajar: GuruMengajarRef | None = None
    tugas: float
    uts: float
    uas: float
    nilai_akhir: float
    status: Literal["Lulus", "Tidak Lulus"]
    created_at: datetime
    updated_at: datetime
