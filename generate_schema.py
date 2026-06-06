from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql, sqlite
from core.database import Base

from features.auth.models import User
from features.siswa.models import Siswa
from features.guru.models import Guru
from features.nilai.models import Nilai
from features.mata_pelajaran.models import MataPelajaran
from features.kelas.models import Kelas
from features.guru_mengajar.models import GuruMengajar


def generate_sql(dialect_name: str) -> str:
    target = postgresql.dialect() if dialect_name == "postgresql" else sqlite.dialect()
    header = f"-- Schema {dialect_name.upper()} — generated from SQLAlchemy ORM"
    lines = [header, ""]

    for table in Base.metadata.sorted_tables:
        lines.append(str(CreateTable(table).compile(dialect=target)).strip() + ";")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    for dialect in ("postgresql", "sqlite"):
        filename = f"schema_{dialect}.sql"
        sql = generate_sql(dialect)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sql)
        print(f"{filename} generated")
