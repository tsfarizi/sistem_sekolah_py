from pydantic import BaseModel, ConfigDict
from core.schemas import GuruRef, KelasRef, MapelRef


class GuruMengajarCreate(BaseModel):
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int


class GuruMengajarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    guru_id: str
    kelas_id: int
    mata_pelajaran_id: int
    guru: GuruRef
    kelas: KelasRef
    mata_pelajaran: MapelRef
