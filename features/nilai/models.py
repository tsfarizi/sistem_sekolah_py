from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Nilai(Base):
    __tablename__ = "nilai"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nis: Mapped[str] = mapped_column(String(20), ForeignKey("siswa.nis", ondelete="CASCADE"), nullable=False)
    guru_mengajar_id: Mapped[int] = mapped_column(Integer, ForeignKey("guru_mengajar.id", ondelete="CASCADE"), nullable=False)
    tugas: Mapped[float] = mapped_column(Float, nullable=False)
    uts: Mapped[float] = mapped_column(Float, nullable=False)
    uas: Mapped[float] = mapped_column(Float, nullable=False)
    nilai_akhir: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    siswa: Mapped["Siswa"] = relationship(back_populates="nilai_list")
    guru_mengajar: Mapped["GuruMengajar"] = relationship(back_populates="nilai_list")
