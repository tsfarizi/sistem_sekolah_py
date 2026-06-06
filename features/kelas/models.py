from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Kelas(Base):
    __tablename__ = "kelas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nama: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    siswa_list: Mapped[list["Siswa"]] = relationship(back_populates="kelas")
    mengajar_list: Mapped[list["GuruMengajar"]] = relationship(back_populates="kelas")
