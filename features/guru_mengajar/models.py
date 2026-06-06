from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class GuruMengajar(Base):
    __tablename__ = "guru_mengajar"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guru_id: Mapped[str] = mapped_column(String(20), ForeignKey("guru.id", ondelete="CASCADE"), nullable=False)
    kelas_id: Mapped[int] = mapped_column(Integer, ForeignKey("kelas.id", ondelete="CASCADE"), nullable=False)
    mata_pelajaran_id: Mapped[int] = mapped_column(Integer, ForeignKey("mata_pelajaran.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("guru_id", "kelas_id", "mata_pelajaran_id", name="uq_guru_kelas_mapel"),
    )

    guru: Mapped["Guru"] = relationship(back_populates="mengajar_list")
    kelas: Mapped["Kelas"] = relationship(back_populates="mengajar_list")
    mata_pelajaran: Mapped["MataPelajaran"] = relationship(back_populates="mengajar_list")
    nilai_list: Mapped[list["Nilai"]] = relationship(back_populates="guru_mengajar", cascade="all, delete-orphan")
