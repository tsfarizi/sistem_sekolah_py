from pydantic import BaseModel, ConfigDict


class GuruMengajarCreate(BaseModel):
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int


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


class GuruMengajarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int
    guru: GuruRef
    kelas: KelasRef
    mata_pelajaran: MapelRef
