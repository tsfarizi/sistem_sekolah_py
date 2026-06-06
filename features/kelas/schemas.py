from typing import Optional
from pydantic import BaseModel, ConfigDict


class KelasCreate(BaseModel):
    nama: str
    wali_kelas_id: Optional[str] = None


class KelasUpdate(BaseModel):
    nama: Optional[str] = None
    wali_kelas_id: Optional[str] = None


class GuruRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str


class KelasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str
    wali_kelas_id: Optional[str] = None
    wali_kelas: Optional[GuruRef] = None
