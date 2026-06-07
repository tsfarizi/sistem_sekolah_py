from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Guru(Base):
    __tablename__ = "guru"
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped["int | None"] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="guru")
    mengajar_list: Mapped[list["GuruMengajar"]] = relationship(back_populates="guru", cascade="all, delete-orphan")
