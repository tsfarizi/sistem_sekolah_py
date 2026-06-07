from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class MataPelajaran(Base):
    __tablename__ = "mata_pelajaran"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nama: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    mengajar_list: Mapped[list["GuruMengajar"]] = relationship(back_populates="mata_pelajaran", cascade="all, delete-orphan")
