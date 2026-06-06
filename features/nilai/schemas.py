from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class GuruRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str


class KelasRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str


class MapelRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str


class SiswaRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nis: str
    nama: str


class GuruMengajarRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int
    guru: Optional[GuruRef] = None
    kelas: Optional[KelasRef] = None
    mata_pelajaran: Optional[MapelRef] = None


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
