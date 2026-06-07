from typing import Optional
from pydantic import BaseModel, ConfigDict


class GuruRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str


class KelasRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str


class MataPelajaranRef(BaseModel):
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
    mata_pelajaran: Optional[MataPelajaranRef] = None

class Message(BaseModel):
    message: str
