from typing import Optional
from pydantic import BaseModel, ConfigDict
from features.nilai.schemas import NilaiResponse


class KelasRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str


class SiswaCreate(BaseModel):
    nis: str
    nama: str
    kelas_id: int
    username: str
    password: str


class SiswaUpdate(BaseModel):
    nama: Optional[str] = None
    kelas_id: Optional[int] = None


class SiswaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nis: str
    nama: str
    kelas_id: int
    kelas: Optional[KelasRef] = None
    user_id: Optional[int] = None


class SiswaWithNilaiResponse(SiswaResponse):
    nilai_list: list[NilaiResponse] = []
