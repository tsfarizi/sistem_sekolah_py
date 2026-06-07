from pydantic import BaseModel, ConfigDict


class KelasCreate(BaseModel):
    nama: str


class KelasUpdate(BaseModel):
    nama: str | None = None


class KelasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nama: str
