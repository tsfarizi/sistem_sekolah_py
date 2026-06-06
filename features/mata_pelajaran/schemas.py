from typing import Optional
from pydantic import BaseModel, ConfigDict


class MataPelajaranCreate(BaseModel):
    nama: str


class MataPelajaranUpdate(BaseModel):
    nama: Optional[str] = None


class MataPelajaranResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str
