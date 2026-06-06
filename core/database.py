from pathlib import Path
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(DATABASE_URL, connect_args={"client_encoding": "utf8"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        return

    is_sqlite = DATABASE_URL.startswith("sqlite")
    filename = "schema_sqlite.sql" if is_sqlite else "schema_postgresql.sql"
    sql_path = Path(__file__).parent.parent / filename

    if not sql_path.exists():
        Base.metadata.create_all(bind=engine)
        return

    raw_sql = sql_path.read_text(encoding="utf-8")

    if is_sqlite:
        statements = raw_sql.split(";")
        with engine.connect() as conn:
            for stmt in statements:
                clean = "\n".join(
                    line for line in stmt.split("\n")
                    if line.strip() and not line.strip().startswith("--")
                ).strip()
                if clean and "CREATE TABLE" in clean:
                    conn.execute(text(clean + ";"))
                    conn.commit()
    else:
        with engine.connect() as conn:
            conn.execute(text(raw_sql))
            conn.commit()
