from pydantic import BaseModel, ConfigDict
from core.schemas import GuruMengajarRef


class GuruCreate(BaseModel):
    id: str | None = None
    nama: str
    username: str
    password: str


class GuruUpdate(BaseModel):
    nama: str | None = None


class GuruResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str
    user_id: int | None = None
    mengajar_list: list[GuruMengajarRef] = []
