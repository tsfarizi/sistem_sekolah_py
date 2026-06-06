from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from features.nilai.utils import hitung_nilai_akhir, tentukan_status


class Nilai(Base):
    __tablename__ = "nilai"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nis: Mapped[str] = mapped_column(String(20), ForeignKey("siswa.nis"), nullable=False)
    guru_mengajar_id: Mapped[int] = mapped_column(Integer, ForeignKey("guru_mengajar.id"), nullable=False)
    tugas: Mapped[float] = mapped_column(Float, nullable=False)
    uts: Mapped[float] = mapped_column(Float, nullable=False)
    uas: Mapped[float] = mapped_column(Float, nullable=False)
    nilai_akhir: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    siswa: Mapped["Siswa"] = relationship(back_populates="nilai_list")
    guru_mengajar: Mapped["GuruMengajar"] = relationship(back_populates="nilai_list")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nis": self.nis,
            "guru_mengajar_id": self.guru_mengajar_id,
            "tugas": self.tugas,
            "uts": self.uts,
            "uas": self.uas,
            "nilai_akhir": self.nilai_akhir,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def kalkulasi(self) -> None:
        self.nilai_akhir = hitung_nilai_akhir(self.tugas, self.uts, self.uas)
        self.status = tentukan_status(self.nilai_akhir)
