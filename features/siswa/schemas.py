from typing import Optional
from pydantic import BaseModel, ConfigDict
from core.schemas import KelasRef
from features.nilai.schemas import NilaiResponse


class SiswaCreate(BaseModel):
    nis: Optional[str] = None
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
