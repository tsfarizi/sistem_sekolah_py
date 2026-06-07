# Sistem Pengolahan Nilai Siswa API

API backend untuk sistem manajemen sekolah yang menangani data siswa, guru, kelas, mata pelajaran, penugasan mengajar, penilaian, dan laporan. Dibangun dengan **FastAPI** menggunakan arsitektur **Vertical Slice Architecture (VSA)** dengan **Clean Architecture** di setiap fitur.

## Fitur

- Autentikasi JWT dengan tiga role: `admin`, `guru`, `siswa`
- Manajemen user, siswa, guru, kelas, dan mata pelajaran
- Penugasan guru ke kelas dan mata pelajaran (junction table `guru_mengajar`)
- Input nilai per komponen (Tugas, UTS, UAS) dengan perhitungan otomatis
- Laporan per kelas dan per siswa

- Auto-generate NIS siswa dan ID guru
- Seed user admin default saat pertama kali dijalankan

## Prasyarat

- Python 3.13+
- PostgreSQL (direkomendasikan) atau SQLite
- `uv` package manager (opsional, bisa juga pakai `pip`)

## Setup & Menjalankan

```bash
# Clone repository
git clone <repo-url>
cd sistem_sekolah_py

# Install dependencies
uv sync
# atau: pip install -r requirements.txt

# Konfigurasi environment
cp .env.example .env   # lalu edit DATABASE_URL dan JWT_SECRET

# Jalankan server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server berjalan di `http://localhost:8000`. Dokumentasi API interaktif tersedia di:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

User admin default:
- Username: `admin`
- Password: `admin123`

## Konfigurasi Database

Buat file `.env` di root project. Tersedia dua opsi database:

```env
# Opsi 1: SQLite (tanpa setup tambahan)
DATABASE_URL=sqlite:///sekolah.db

# Opsi 2: PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/sekolah_db

JWT_SECRET=jwt-secret-key-change-in-production
```

Untuk PostgreSQL, pastikan database sudah dibuat:

```sql
CREATE DATABASE sekolah_db;
```

## Database Migration (Alembic)

Proyek ini menggunakan **Alembic** untuk mengelola perubahan struktur database secara aman tanpa kehilangan data. Alembic melacak perubahan di model SQLAlchemy dan menghasilkan script migration.

### Setup Awal (hanya sekali)

Setelah clone, jalankan migration pertama untuk membuat semua tabel:

```bash
uv run alembic upgrade head
```

### Alur Kerja Sehari-hari

Setiap kali ada perubahan struktur data (tambah kolom, tabel baru, ubah constraint, dll.), ikuti langkah berikut:

```bash
# 1. Generate script migration otomatis dari perubahan model
uv run alembic revision --autogenerate -m "deskripsi perubahan"

# 2. Review file migration yang dihasilkan di alembic/versions/
#    Pastikan tidak ada operasi yang salah atau berbahaya

# 3. Jalankan migration
uv run alembic upgrade head
```

### Perintah Alembik yang Sering Digunakan

| Perintah | Kegunaan |
|----------|----------|
| `alembic upgrade head` | Jalankan semua migration ke versi terbaru |
| `alembic downgrade -1` | Kembalikan 1 migration ke belakang |
| `alembic revision --autogenerate -m "..."` | Buat migration otomatis dari perubahan model |
| `alembic current` | Lihat versi migration database saat ini |
| `alembic history` | Lihat riwayat semua migration |
| `alembic upgrade +2` | Maju 2 migration ke depan |
| `alembic stamp head` | Tandai database sebagai versi terbaru (tanpa menjalankan migration) |

### Catatan Penting

- Migration autogenerate mendeteksi perubahan seperti: kolom baru/hapus, tipe data berubah, constraint baru, tabel baru
- Beberapa perubahan (rename kolom, rename tabel) tidak bisa dideteksi otomatis — harus ditulis manual di script migration
- Selalu review file migration sebelum dijalankan di production
- Untuk development, jika database masih kosong bisa langsung hapus DB dan restart — `init_db()` akan membuat ulang tabel

## Generate Skema SQL (opsional)

Tiga file skema SQL tersedia untuk masing-masing dialek database. Untuk me-regenerate semua file skema dari definisi model terbaru:

```bash
uv run python generate_schema.py
```

Menghasilkan tiga file:

| File | Dialek |
|------|--------|
| `schema_postgresql.sql` | PostgreSQL |
| `schema_sqlite.sql` | SQLite |
| `schema_mysql.sql` | MySQL |

## Memulai Menggunakan

Setelah server berjalan, urutan operasi yang direkomendasikan:

1. **Login sebagai admin** — `POST /api/auth/login` dengan `admin` / `admin123`
2. **Buat kelas** — `POST /api/kelas`
3. **Buat mata pelajaran** — `POST /api/mata-pelajaran`
4. **Buat guru** — `POST /api/guru` (otomatis membuat user login untuk guru)
5. **Buat siswa** — `POST /api/siswa` (otomatis membuat user login untuk siswa)
6. **Assign guru ke kelas & mata pelajaran** — `POST /api/guru-mengajar`
7. **Input nilai** — `POST /api/nilai`
8. **Lihat laporan** — `GET /api/laporan`

Guru dapat login dan menginput nilai untuk kelas yang dia ajar. Siswa dapat login dan melihat nilainya sendiri.

## Struktur Proyek

```
sistem_sekolah_py/
├── app/                        # Application entry point
│   ├── main.py                 # FastAPI app, lifespan, middleware, exception handlers
│   ├── config.py               # Env variable loading

├── core/                       # Shared infrastructure (cross-cutting)
│   ├── database.py             # SQLAlchemy engine, session, init_db
│   ├── security.py             # JWT encode/decode, bcrypt hash/verify
│   ├── dependencies.py         # FastAPI Depends: get_current_user, require_admin, require_any_role
│   ├── exceptions.py           # Domain exceptions (NotFound, BadRequest, Forbidden, etc.)
│   └── schemas.py              # Shared Ref schemas (GuruRef, KelasRef, etc.)
├── features/                   # Business features (vertical slices)
│   ├── auth/                   # Authentication + User CRUD
│   │   ├── models.py           # User ORM model
│   │   ├── schemas.py          # Pydantic DTOs (request/response)
│   │   ├── repository.py       # Data access (all DB queries)
│   │   ├── service.py          # Business logic
│   │   └── router.py           # HTTP endpoints
│   ├── siswa/                  # Student management
│   ├── guru/                   # Teacher management
│   ├── kelas/                  # Class management
│   ├── mata_pelajaran/         # Subject management
│   ├── guru_mengajar/          # Teaching assignments (junction)
│   ├── nilai/                  # Grade management
│   │   ├── utils.py            # Pure functions: validasi, hitung nilai, laporan
│   │   └── ...
│   └── laporan/                # Report generation
├── schema_postgresql.sql       # DDL schema for PostgreSQL
├── schema_sqlite.sql           # DDL schema for SQLite
├── openapi.yaml                # OpenAPI 3.0 specification
├── pyproject.toml
└── .env
```

## Arsitektur

Proyek ini mengadopsi **Vertical Slice Architecture (VSA)** yang dikombinasikan dengan prinsip **Clean Architecture** di setiap fitur. Setiap fitur adalah modul mandiri dengan lapisan yang terpisah secara ketat.

```mermaid
graph TB
    subgraph "Application Layer"
        ROUTER["Router<br/>(HTTP Endpoints)"]
    end

    subgraph "Domain Layer"
        SVC["Service<br/>(Business Logic)"]
        SCHEMA["Schemas<br/>(DTOs / Validasi)"]
        UTILS["Utils<br/>(Pure Functions)"]
    end

    subgraph "Data Layer"
        REPO["Repository<br/>(Data Access)"]
        MODEL["Model<br/>(ORM Entity)"]
    end

    subgraph "Infrastructure"
        DB["Database<br/>(PostgreSQL/SQLite)"]
        AUTH["Core Dependencies<br/>(JWT, Role Guards)"]
        EXC["Domain Exceptions<br/>(404, 400, 403, 401)"]
    end

    ROUTER -->|"Depends"| AUTH
    ROUTER -->|"calls"| SVC
    SVC -->|"calls"| REPO
    SVC -->|"uses"| SCHEMA
    SVC -->|"uses"| UTILS
    SVC -->|"raises"| EXC
    REPO -->|"queries"| MODEL
    MODEL -->|"maps to"| DB
    AUTH -->|"validates"| EXC
```

### Prinsip Arsitektur

| Prinsip | Implementasi |
|---------|--------------|
| **Dependency Rule** | Dependensi mengalir ke dalam: Router → Service → Repository → Model. Lapisan inner tidak tahu lapisan outer. |
| **Separation of Concerns** | Setiap file punya satu tanggung jawab: router hanya HTTP, service hanya bisnis, repository hanya query. |
| **Domain Exceptions** | Service tidak impor `HTTPException`. Semua error dari service adalah domain exception yang diterjemahkan ke HTTP response oleh handler di `app/main.py`. |
| **Vertical Slice** | Setiap fitur (auth, siswa, guru, dll.) adalah modul mandiri dengan models, schemas, repository, service, router sendiri. |

### Alur Request

```mermaid
sequenceDiagram
    participant Client
    participant Router
    participant Auth as Core Dependencies
    participant Service
    participant Repository
    participant Database

    Client->>Router: HTTP Request
    Router->>Auth: get_current_user()
    Auth->>Database: decode JWT, query user
    Auth-->>Router: CurrentUser
    Router->>Auth: require_admin()
    alt Role tidak sesuai
        Auth-->>Client: 403 Forbidden
    else Role sesuai
        Auth-->>Router: OK
        Router->>Service: panggil service function
        Service->>Repository: panggil repository function
        Repository->>Database: SQL query
        Database-->>Repository: result
        Repository-->>Service: entity/list
        Service-->>Router: hasil (atau raise domain exception)
        Router-->>Client: HTTP Response
    end
```

### Lapisan Fitur — Contoh `features/nilai/`

```mermaid
graph LR
    subgraph "features/nilai/"
        R["router.py<br/>GET/POST/PUT/DELETE<br/>/api/nilai"]
        S["service.py<br/>list_nilai()<br/>create_new_nilai()<br/>update_existing_nilai()<br/>delete_existing_nilai()"]
        REP["repository.py<br/>get_nilai_filtered()<br/>get_nilai_by_id()<br/>create_nilai()<br/>update_nilai()<br/>delete_nilai()"]
        M["models.py<br/>class Nilai(Base)"]
        U["utils.py<br/>validasi_nilai()<br/>hitung_nilai_akhir()<br/>tentukan_status()<br/>generate_laporan_siswa()"]
        SCH["schemas.py<br/>NilaiCreate<br/>NilaiUpdate<br/>NilaiResponse"]
    end

    R -->|"Depends(require_any_role)"| R
    R --> S
    S --> REP
    S --> U
    S --> SCH
    REP --> M
```

## Formula Nilai

Nilai akhir dihitung otomatis oleh server menggunakan rumus:

```
Nilai Akhir = (30% × Tugas) + (30% × UTS) + (40% × UAS)
```

Status kelulusan:

```
Lulus       → Nilai Akhir ≥ 70
Tidak Lulus → Nilai Akhir < 70
```

Implementasi ada di `features/nilai/utils.py` sebagai pure functions:

- `validasi_nilai(nilai: float) -> bool` — memastikan nilai 0–100
- `hitung_nilai_akhir(tugas, uts, uas) -> float` — menghitung rata-rata tertimbang
- `tentukan_status(nilai_akhir) -> str` — menentukan Lulus/Tidak Lulus

## Role & Otorisasi

| Role | Hak Akses |
|------|-----------|
| **admin** | Full CRUD semua entitas. Reset password user. Akses laporan. |
| **guru** | Input dan update nilai untuk kelas & mata pelajaran yang dia ajar. Lihat semua nilai. Lihat laporan. |
| **siswa** | Hanya lihat nilai dan laporan milik sendiri. Ganti password sendiri. |

Otorisasi diterapkan melalui dependency injection di `core/dependencies.py`:

- `require_admin` — membatasi endpoint ke admin saja
- `require_any_role("admin", "guru")` — membatasi ke admin atau guru
- Data scoping (siswa hanya lihat data sendiri) dilakukan di service layer

## API Endpoints

| Method | Endpoint | Role | Deskripsi |
|--------|----------|------|-----------|
| POST | `/api/auth/login` | Public | Login, dapatkan JWT token |
| PUT | `/api/auth/change-password` | Semua | Ganti password sendiri |
| PUT | `/api/auth/reset-password/{id}` | Admin | Admin reset password user |
| GET | `/api/users` | Semua | List semua user |
| GET | `/api/users/{id}` | Semua | Detail user |
| POST | `/api/users` | Admin | Tambah user baru |
| PUT | `/api/users/{id}` | Admin | Update user |
| DELETE | `/api/users/{id}` | Admin | Hapus user |
| GET | `/api/kelas` | Semua | List kelas |
| GET | `/api/kelas/{id}` | Semua | Detail kelas |
| POST | `/api/kelas` | Admin | Tambah kelas |
| PUT | `/api/kelas/{id}` | Admin | Update kelas |
| DELETE | `/api/kelas/{id}` | Admin | Hapus kelas |
| GET | `/api/mata-pelajaran` | Semua | List mata pelajaran |
| GET | `/api/mata-pelajaran/{id}` | Semua | Detail mata pelajaran |
| POST | `/api/mata-pelajaran` | Admin | Tambah mata pelajaran |
| PUT | `/api/mata-pelajaran/{id}` | Admin | Update mata pelajaran |
| DELETE | `/api/mata-pelajaran/{id}` | Admin | Hapus mata pelajaran |
| GET | `/api/siswa` | Semua | List siswa (filter: `?kelas_id=`) |
| GET | `/api/siswa/{nis}` | Semua | Detail siswa + nilai |
| POST | `/api/siswa` | Admin | Tambah siswa (auto-create user) |
| PUT | `/api/siswa/{nis}` | Admin | Update siswa |
| DELETE | `/api/siswa/{nis}` | Admin | Hapus siswa + user |
| GET | `/api/guru` | Semua | List guru |
| GET | `/api/guru/{id}` | Semua | Detail guru |
| POST | `/api/guru` | Admin | Tambah guru (auto-create user) |
| PUT | `/api/guru/{id}` | Admin | Update guru |
| DELETE | `/api/guru/{id}` | Admin | Hapus guru + user |
| GET | `/api/guru-mengajar` | Semua | List assignment (filter: `?guru_id=&kelas_id=&mata_pelajaran_id=`) |
| GET | `/api/guru-mengajar/{id}` | Semua | Detail assignment |
| POST | `/api/guru-mengajar` | Admin | Assign guru ke kelas & mata pelajaran |
| DELETE | `/api/guru-mengajar/{id}` | Admin | Hapus assignment |
| GET | `/api/nilai` | Semua | List nilai (filter: `?kelas_id=&mata_pelajaran_id=`, siswa hanya lihat sendiri) |
| GET | `/api/nilai/{id}` | Semua | Detail nilai |
| GET | `/api/nilai/siswa/{nis}` | Semua | Nilai per siswa (siswa hanya lihat sendiri) |
| POST | `/api/nilai` | Admin, Guru | Input nilai (auto-hitung) |
| PUT | `/api/nilai/{id}` | Admin, Guru | Update nilai (auto-hitung ulang) |
| DELETE | `/api/nilai/{id}` | Admin | Hapus nilai |
| GET | `/api/laporan` | Admin, Guru | Laporan per kelas |
| GET | `/api/laporan/siswa/{nis}` | Admin, Guru | Laporan individu siswa |

## Entity Relationship

```mermaid
erDiagram
    User ||--o| Siswa : "1:1"
    User ||--o| Guru : "1:1"
    Siswa ||--o{ Nilai : "has"
    Guru ||--o{ GuruMengajar : "teaches"
    Kelas ||--o{ GuruMengajar : "in"
    Kelas ||--o{ Siswa : "contains"
    MataPelajaran ||--o{ GuruMengajar : "subject"
    GuruMengajar ||--o{ Nilai : "graded in"

    User {
        int id PK
        string username UK
        string password_hash
        string role
        string nama
    }

    Siswa {
        string nis PK
        string nama
        int kelas_id FK
        int user_id FK
    }

    Guru {
        string id PK
        string nama
        int user_id FK
    }

    Kelas {
        int id PK
        string nama
    }

    MataPelajaran {
        int id PK
        string nama
    }

    GuruMengajar {
        int id PK
        string guru_id FK
        int kelas_id FK
        int mata_pelajaran_id FK
    }

    Nilai {
        int id PK
        string nis FK
        int guru_mengajar_id FK
        float tugas
        float uts
        float uas
        float nilai_akhir
        string status
    }
```

## Code Convention

### Penamaan

| Konteks | Konvensi | Contoh |
|---------|----------|--------|
| File | `snake_case` | `guru_mengajar`, `mata_pelajaran` |
| Model class | `PascalCase`, singular | `Siswa`, `GuruMengajar` |
| Repository functions | `snake_case`, deskriptif | `get_siswa_by_nis()`, `get_nilai_filtered()` |
| Service functions | `snake_case`, action-oriented | `create_new_siswa()`, `update_existing_nilai()` |
| Router endpoint names | `snake_case` | `def get_all(...)`, `def create(...)` |
| Domain exceptions | `PascalCase`, suffix `Exception` | `NotFoundException`, `ForbiddenException` |
| Detail message | Bahasa Indonesia | `"Kelas tidak ditemukan"` |
| Commit message | Bahasa Indonesia, imperative | `"tambah fitur absensi siswa"` |

### Struktur Wajib per Fitur

Setiap fitur di bawah `features/` harus memiliki file berikut:

```
features/<nama_fitur>/
├── __init__.py          # Kosong
├── models.py            # SQLAlchemy ORM entity — hanya definisi kolom & relationship
├── schemas.py           # Pydantic DTOs — request/response, validasi
├── repository.py        # Data access — semua query SQLAlchemy disini
├── service.py           # Business logic — orkestrasi, validasi bisnis, raise domain exception
└── router.py            # HTTP endpoints — parameter parsing, panggil service, return response
```

### Aturan per Layer

**Router** (`router.py`)
- Hanya berisi dekorator FastAPI (`@router.get`, dll.) dan pemanggilan service
- Otorisasi via `Depends(require_admin)` atau `Depends(require_any_role(...))` — jangan inline `if role != "admin"`
- Import `CurrentUser` dari `core.dependencies`, bukan dari `features.auth.models`
- Tidak boleh import repository langsung
- Tidak boleh membuat instance model

**Service** (`service.py`)
- Semua business logic, validasi, dan orkestrasi
- Raise domain exception (`NotFoundException`, `BadRequestException`, dll.) — JANGAN import `HTTPException`
- Semua akses database melalui repository — JANGAN `db.query(Model)` langsung
- Jika butuh data dari fitur lain, panggil repository fitur tersebut — JANGAN `db.query(ModelLain)`

**Repository** (`repository.py`)
- Satu-satunya tempat yang boleh menggunakan `db.query()`, `db.add()`, `db.commit()`, dll.
- Function name harus deskriptif: `get_by_id()`, `get_by_username()`, `create_with_user()`
- Boleh melakukan operasi composite untuk aggregate root (contoh: `create_siswa_with_user()` membuat User + Siswa dalam satu transaksi)
- Boleh mengimpor model dari fitur lain untuk `joinedload` — tapi seminimal mungkin

**Model** (`models.py`)
- Hanya definisi kolom (`mapped_column`), relationship, dan constraint database
- Tidak boleh ada business logic (method seperti `kalkulasi()`, `to_dict()`)
- Tidak boleh import framework web (FastAPI, starlette)

**Utils** (`utils.py`) — opsional, buat jika ada pure functions
- Pure functions: tidak ada side effect, tidak akses database, tidak import FastAPI
- Contoh: validasi, kalkulasi, formatting

## Menambahkan Fitur Baru

Ikuti langkah-langkah berikut untuk menambah fitur baru dengan konsisten. Contoh: menambahkan fitur **Absensi**.

### Langkah 1: Buat struktur folder

```
features/absensi/
├── __init__.py
├── models.py
├── schemas.py
├── repository.py
├── service.py
└── router.py
```

### Langkah 2: Definisikan model (`models.py`)

```python
from datetime import date
from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Absensi(Base):
    __tablename__ = "absensi"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nis: Mapped[str] = mapped_column(String(20), ForeignKey("siswa.nis", ondelete="CASCADE"))
    tanggal: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)

    siswa: Mapped["Siswa"] = relationship(back_populates="absensi_list")
```

### Langkah 3: Definisikan schema request/response (`schemas.py`)

```python
from pydantic import BaseModel, ConfigDict
from datetime import date

class AbsensiCreate(BaseModel):
    nis: str
    tanggal: date
    status: str

class AbsensiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nis: str
    tanggal: date
    status: str
```

### Langkah 4: Buat repository (`repository.py`)

```python
from sqlalchemy.orm import Session
from features.absensi.models import Absensi

def get_all(db: Session) -> list[Absensi]:
    return db.query(Absensi).all()

def get_by_id(db: Session, absensi_id: int) -> Absensi | None:
    return db.query(Absensi).filter(Absensi.id == absensi_id).first()

def get_by_siswa(db: Session, nis: str) -> list[Absensi]:
    return db.query(Absensi).filter(Absensi.nis == nis).all()

def create(db: Session, absensi: Absensi) -> Absensi:
    db.add(absensi)
    db.commit()
    db.refresh(absensi)
    return absensi
```

### Langkah 5: Buat service (`service.py`)

```python
from sqlalchemy.orm import Session
from features.absensi.models import Absensi
from features.absensi.repository import get_all, get_by_id, get_by_siswa, create
from features.absensi.schemas import AbsensiCreate
from core.exceptions import NotFoundException, BadRequestException

def list_absensi(db: Session) -> list[Absensi]:
    return get_all(db)

def detail_absensi(db: Session, absensi_id: int) -> Absensi:
    result = get_by_id(db, absensi_id)
    if not result:
        raise NotFoundException("Absensi tidak ditemukan")
    return result

def create_absensi(db: Session, data: AbsensiCreate) -> Absensi:
    if data.status not in ("Hadir", "Izin", "Sakit", "Alpa"):
        raise BadRequestException("Status tidak valid")
    absensi = Absensi(nis=data.nis, tanggal=data.tanggal, status=data.status)
    return create(db, absensi)

def list_absensi_siswa(db: Session, nis: str) -> list[Absensi]:
    return get_by_siswa(db, nis)
```

### Langkah 6: Buat router (`router.py`)

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.dependencies import get_db, require_any_role, CurrentUser
from features.absensi.schemas import AbsensiCreate, AbsensiResponse
from features.absensi.service import list_absensi, detail_absensi, create_absensi, list_absensi_siswa

router = APIRouter(prefix="/api/absensi", tags=["Absensi"])

@router.get("", response_model=list[AbsensiResponse])
def get_all(db: Session = Depends(get_db), _: CurrentUser = Depends(require_any_role("admin", "guru"))):
    return list_absensi(db)

@router.get("/siswa/{nis}", response_model=list[AbsensiResponse])
def get_by_siswa(nis: str, db: Session = Depends(get_db), _: CurrentUser = Depends(require_any_role("admin", "guru"))):
    return list_absensi_siswa(db, nis)

@router.get("/{id}", response_model=AbsensiResponse)
def get_by_id(id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_any_role("admin", "guru"))):
    return detail_absensi(db, id)

@router.post("", response_model=AbsensiResponse, status_code=status.HTTP_201_CREATED)
def create(data: AbsensiCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_any_role("admin", "guru"))):
    return create_absensi(db, data)
```

### Langkah 7: Daftarkan router di `app/main.py`

```python
from features.absensi.router import router as absensi_router

# Tambahkan di dalam blok app.include_router:
app.include_router(absensi_router)
```
### Checklist Sebelum Commit

- [ ] Model tidak mengandung business logic
- [ ] Repository menangani semua query database
- [ ] Service menggunakan domain exception, bukan `HTTPException`
- [ ] Router menggunakan `Depends(require_admin)` atau `Depends(require_any_role(...))`
- [ ] Router tidak import repository atau model secara langsung
- [ ] Schema response menggunakan `ConfigDict(from_attributes=True)`
- [ ] Router terdaftar di `app/main.py`
- [ ] Fitur baru sudah diuji melalui Swagger UI (`/docs`)
