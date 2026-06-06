from typing import Optional
from pydantic import BaseModel, ConfigDict


class GuruCreate(BaseModel):
    id: Optional[str] = None
    nama: str
    username: str
    password: str


class GuruUpdate(BaseModel):
    nama: Optional[str] = None


class GuruMengajarRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int


class GuruResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str
    user_id: Optional[int] = None
    mengajar_list: list[GuruMengajarRef] = []
