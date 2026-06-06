from typing import Optional
from pydantic import BaseModel, ConfigDict
from core.schemas import GuruMengajarRef


class GuruCreate(BaseModel):
    id: Optional[str] = None
    nama: str
    username: str
    password: str


class GuruUpdate(BaseModel):
    nama: Optional[str] = None


class GuruResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nama: str
    user_id: Optional[int] = None
    mengajar_list: list[GuruMengajarRef] = []
