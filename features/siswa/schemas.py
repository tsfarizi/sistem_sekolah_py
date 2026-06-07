from pydantic import BaseModel, ConfigDict
from core.schemas import KelasRef
from features.nilai.schemas import NilaiResponse


class SiswaCreate(BaseModel):
    nis: str | None = None
    nama: str
    kelas_id: int
    username: str
    password: str


class SiswaUpdate(BaseModel):
    nama: str | None = None
    kelas_id: int | None = None


class SiswaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nis: str
    nama: str
    kelas_id: int
    kelas: KelasRef | None = None
    user_id: int | None = None


class SiswaWithNilaiResponse(SiswaResponse):
    nilai_list: list[NilaiResponse] = []
