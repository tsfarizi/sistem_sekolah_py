from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Siswa(Base):
    __tablename__ = "siswa"
    nis: Mapped[str] = mapped_column(String(20), primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    kelas_id: Mapped[int] = mapped_column(Integer, ForeignKey("kelas.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="siswa")
    kelas: Mapped["Kelas"] = relationship(back_populates="siswa_list")
    nilai_list: Mapped[list["Nilai"]] = relationship(back_populates="siswa", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "nis": self.nis,
            "nama": self.nama,
            "kelas_id": self.kelas_id,
            "user_id": self.user_id,
        }

    def get_nilai_akhir(self) -> list:
        return self.nilai_list
