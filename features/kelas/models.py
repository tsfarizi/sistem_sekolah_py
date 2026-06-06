from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Kelas(Base):
    __tablename__ = "kelas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nama: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    wali_kelas_id: Mapped[Optional[str]] = mapped_column(String(20), ForeignKey("guru.id"), nullable=True)

    wali_kelas: Mapped[Optional["Guru"]] = relationship(back_populates="wali_kelas_list")
    siswa_list: Mapped[list["Siswa"]] = relationship(back_populates="kelas")
    mengajar_list: Mapped[list["GuruMengajar"]] = relationship(back_populates="kelas")
