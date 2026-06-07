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
    guru: GuruRef | None = None
    kelas: KelasRef | None = None
    mata_pelajaran: MataPelajaranRef | None = None

class Message(BaseModel):
    message: str
