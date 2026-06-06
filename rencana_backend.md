# Rencana Implementasi Backend — Python FastAPI

## Tech Stack
| Komponen | Teknologi |
|----------|-----------|
| Bahasa | Python (latest) |
| Framework | FastAPI (latest) |
| Server | Uvicorn (latest) |
| ORM | SQLAlchemy (latest) |
| Database | SQLite (`sekolah.db`) |
| Auth | PyJWT + passlib[bcrypt] (latest) |
| Validasi | Pydantic (latest) |
| Arsitektur | Vertical Slice + Clean Architecture |

---

## Arsitektur

```
Setiap fitur = Vertical Slice
Setiap Slice = Clean Architecture di dalamnya:
  router.py   → Presentation (API endpoint)
  service.py  → Application (business logic)
  repository.py → Data (DB queries)
  models.py   → Domain (ORM entities)
  schemas.py  → Domain (Pydantic DTOs)
```

---

## Struktur Proyek

```
sistem_sekolah_py/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point, CORS, router registration
│   └── config.py            # Settings: DB URL, JWT_SECRET, ALGORITHM, TOKEN_EXPIRE
├── core/
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy engine, SessionLocal, Base, get_db()
│   ├── security.py          # hash_password(), verify_password(), create_access_token(), decode_token()
│   ├── exceptions.py        # Custom exceptions (NotFoundException, UnauthorizedException, etc.)
│   └── dependencies.py      # get_db (dependency), get_current_user (dependency + JWT guard)
├── features/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py        # POST /api/auth/login
│   │   ├── service.py       # authenticate() — verifikasi username + password
│   │   ├── schemas.py       # LoginRequest, LoginResponse (with token + role)
│   │   └── models.py        # ORM: User (id, username, password_hash, role, nama)
│   ├── siswa/
│   │   ├── __init__.py
│   │   ├── router.py        # CRUD /api/siswa
│   │   ├── service.py       # get_all(), get_by_nis(), create(), update(), delete()
│   │   ├── schemas.py       # SiswaCreate, SiswaUpdate, SiswaResponse
│   │   ├── models.py        # ORM: Siswa (nis PK, nama, kelas, user_id FK)
│   │   └── repository.py    # DB operations (SQLAlchemy queries)
│   ├── guru/
│   │   ├── __init__.py
│   │   ├── router.py        # CRUD /api/guru
│   │   ├── service.py       # get_all(), get_by_id(), create(), update(), delete()
│   │   ├── schemas.py       # GuruCreate, GuruUpdate, GuruResponse
│   │   ├── models.py        # ORM: Guru (id PK, nama, mata_pelajaran, user_id FK)
│   │   └── repository.py    # DB operations
│   ├── nilai/
│   │   ├── __init__.py
│   │   ├── router.py        # CRUD /api/nilai + GET /api/nilai/siswa/{nis}
│   │   ├── service.py       # get_all(), get_by_id(), get_by_siswa(), create(), update(), delete()
│   │   ├── schemas.py       # NilaiCreate, NilaiUpdate, NilaiResponse
│   │   ├── models.py        # ORM: Nilai (id PK, nis FK, guru_id FK, mapel, tugas, uts, uas, nilai_akhir, status)
│   │   ├── repository.py    # DB operations
│   │   └── utils.py         # ★ FUNGSI TERSTRUKTUR (lihat section di bawah)
│   └── laporan/
│       ├── __init__.py
│       ├── router.py        # GET /api/laporan?kelas=X  +  GET /api/laporan/siswa/{nis}
│       ├── service.py       # generate_by_kelas(), generate_by_siswa()
│       └── schemas.py       # LaporanKelasResponse, LaporanSiswaResponse
├── requirements.txt
├── rencana_backend.md       # File ini
└── openapi.yaml             # Spesifikasi OpenAPI
```

---

## Database Schema (SQLite)

### Tabel `users`

| Kolom | Tipe | Constraint | Deskripsi |
|-------|------|------------|-----------|
| id | Integer | PK, Auto-increment | ID user |
| username | String(50) | UNIQUE, NOT NULL | Username login |
| password_hash | String(255) | NOT NULL | Hashed password (bcrypt) |
| role | String(20) | NOT NULL | `admin`, `guru`, `siswa` |
| nama | String(100) | NOT NULL | Nama asli pengguna |
| created_at | DateTime | Default: now | Waktu pembuatan |

### Tabel `siswa`

| Kolom | Tipe | Constraint | Deskripsi |
|-------|------|------------|-----------|
| nis | String(20) | PK | Nomor Induk Siswa (unik) |
| nama | String(100) | NOT NULL | Nama lengkap siswa |
| kelas | String(20) | NOT NULL | Kelas (contoh: X-A, XI-B, XII-C) |
| user_id | Integer | FK → users.id, UNIQUE | Link ke account login |

### Tabel `guru`

| Kolom | Tipe | Constraint | Deskripsi |
|-------|------|------------|-----------|
| id | String(20) | PK | ID Guru (kode unik) |
| nama | String(100) | NOT NULL | Nama lengkap guru |
| mata_pelajaran | String(50) | NOT NULL | Mata pelajaran yang diampu |
| user_id | Integer | FK → users.id, UNIQUE | Link ke account login |

### Tabel `nilai`

| Kolom | Tipe | Constraint | Deskripsi |
|-------|------|------------|-----------|
| id | Integer | PK, Auto-increment | ID nilai |
| nis | String(20) | FK → siswa.nis, NOT NULL | Siswa yang dinilai |
| guru_id | String(20) | FK → guru.id, NOT NULL | Guru yang memberi nilai |
| mata_pelajaran | String(50) | NOT NULL | Mata pelajaran |
| tugas | Float | NOT NULL | Nilai Tugas (0-100) |
| uts | Float | NOT NULL | Nilai UTS (0-100) |
| uas | Float | NOT NULL | Nilai UAS (0-100) |
| nilai_akhir | Float | NOT NULL | Hasil kalkulasi otomatis |
| status | String(20) | NOT NULL | `Lulus` / `Tidak Lulus` |
| created_at | DateTime | Default: now | Waktu input |
| updated_at | DateTime | Default: now, onupdate | Waktu update terakhir |

---

## API Endpoints

### Auth

| Method | Path | Auth | Deskripsi |
|--------|------|------|-----------|
| POST | `/api/auth/login` | No | Login, return JWT token + role |

### Siswa

| Method | Path | Auth | Role | Deskripsi |
|--------|------|------|------|-----------|
| GET | `/api/siswa` | Yes | Admin, Guru | List semua siswa |
| GET | `/api/siswa/{nis}` | Yes | All | Detail siswa by NIS |
| POST | `/api/siswa` | Yes | Admin | Tambah siswa baru |
| PUT | `/api/siswa/{nis}` | Yes | Admin | Update data siswa |
| DELETE | `/api/siswa/{nis}` | Yes | Admin | Hapus siswa |

### Guru

| Method | Path | Auth | Role | Deskripsi |
|--------|------|------|------|-----------|
| GET | `/api/guru` | Yes | Admin | List semua guru |
| GET | `/api/guru/{id}` | Yes | All | Detail guru by ID |
| POST | `/api/guru` | Yes | Admin | Tambah guru baru |
| PUT | `/api/guru/{id}` | Yes | Admin | Update data guru |
| DELETE | `/api/guru/{id}` | Yes | Admin | Hapus guru |

### Nilai

| Method | Path | Auth | Role | Deskripsi |
|--------|------|------|------|-----------|
| GET | `/api/nilai` | Yes | Admin, Guru | List semua nilai |
| GET | `/api/nilai/{id}` | Yes | All | Detail nilai by ID |
| GET | `/api/nilai/siswa/{nis}` | Yes | All | Nilai milik siswa tertentu |
| POST | `/api/nilai` | Yes | Guru, Admin | Input nilai baru (auto kalkulasi) |
| PUT | `/api/nilai/{id}` | Yes | Guru, Admin | Update nilai (auto kalkulasi ulang) |
| DELETE | `/api/nilai/{id}` | Yes | Admin | Hapus nilai |

### Laporan

| Method | Path | Auth | Role | Deskripsi |
|--------|------|------|------|-----------|
| GET | `/api/laporan` | Yes | Admin, Guru | Laporan per kelas (query: `?kelas=X`) |
| GET | `/api/laporan/siswa/{nis}` | Yes | All | Laporan individu siswa (semua nilai + status) |

---

## OOP Implementation (min 2 class)

### Class `Siswa` — `features/siswa/models.py`
```python
class Siswa(Base):
    __tablename__ = "siswa"
    nis: Mapped[str] = mapped_column(String(20), primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    kelas: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="siswa")
    nilai_list: Mapped[list["Nilai"]] = relationship(back_populates="siswa")

    def to_dict(self) -> dict:
        """Convert ORM object to dictionary"""
        ...

    def get_nilai_akhir(self) -> list:
        """Get all nilai for this student"""
        ...
```

### Class `Guru` — `features/guru/models.py`
```python
class Guru(Base):
    __tablename__ = "guru"
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    mata_pelajaran: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="guru")
    nilai_list: Mapped[list["Nilai"]] = relationship(back_populates="guru")

    def to_dict(self) -> dict:
        ...
```

### Class `Nilai` — `features/nilai/models.py`
```python
class Nilai(Base):
    __tablename__ = "nilai"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nis: Mapped[str] = mapped_column(String(20), ForeignKey("siswa.nis"), nullable=False)
    guru_id: Mapped[str] = mapped_column(String(20), ForeignKey("guru.id"), nullable=False)
    mata_pelajaran: Mapped[str] = mapped_column(String(50), nullable=False)
    tugas: Mapped[float] = mapped_column(Float, nullable=False)
    uts: Mapped[float] = mapped_column(Float, nullable=False)
    uas: Mapped[float] = mapped_column(Float, nullable=False)
    nilai_akhir: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    siswa: Mapped["Siswa"] = relationship(back_populates="nilai_list")
    guru: Mapped["Guru"] = relationship(back_populates="nilai_list")

    def to_dict(self) -> dict:
        ...

    def kalkulasi(self) -> None:
        """Hitung nilai_akhir dan tentukan status"""
        self.nilai_akhir = hitung_nilai_akhir(self.tugas, self.uts, self.uas)
        self.status = tentukan_status(self.nilai_akhir)
```

---

## Structured Programming (min 3 fungsi)

Semua fungsi terstruktur disimpan di `features/nilai/utils.py`:

```python
# features/nilai/utils.py

def validasi_nilai(nilai: float) -> bool:
    """
    Validasi apakah nilai berada dalam rentang 0 - 100.
    Return True jika valid, False jika tidak.
    """
    return 0.0 <= nilai <= 100.0


def hitung_nilai_akhir(tugas: float, uts: float, uas: float) -> float:
    """
    Menghitung nilai akhir dengan rumus:
    Nilai Akhir = (30% × Tugas) + (30% × UTS) + (40% × UAS)
    Return nilai akhir (float), dibulatkan 2 desimal.
    """
    return round(0.3 * tugas + 0.3 * uts + 0.4 * uas, 2)


def tentukan_status(nilai_akhir: float) -> str:
    """
    Menentukan status kelulusan.
    Return 'Lulus' jika nilai_akhir >= 70, selain itu 'Tidak Lulus'.
    """
    return "Lulus" if nilai_akhir >= 70.0 else "Tidak Lulus"


def generate_laporan_siswa(nilai_list: list[dict]) -> dict:
    """
    Menghasilkan ringkasan laporan untuk satu siswa.
    Input: list nilai dalam bentuk dict
    Output: dict dengan ringkasan (rata-rata, jumlah lulus, dll.)
    """
    if not nilai_list:
        return {"rata_rata": 0, "jumlah_mapel": 0, "lulus": 0, "tidak_lulus": 0, "detail": []}

    total = sum(n["nilai_akhir"] for n in nilai_list)
    jumlah = len(nilai_list)
    lulus = sum(1 for n in nilai_list if n["status"] == "Lulus")
    
    return {
        "rata_rata": round(total / jumlah, 2),
        "jumlah_mapel": jumlah,
        "lulus": lulus,
        "tidak_lulus": jumlah - lulus,
        "detail": nilai_list
    }


def generate_laporan_kelas(nilai_list: list[dict], kelas: str) -> dict:
    """
    Menghasilkan laporan untuk satu kelas.
    Input: list nilai (sudah difilter per kelas), nama kelas
    Output: dict dengan statistik kelas
    """
    if not nilai_list:
        return {"kelas": kelas, "jumlah_siswa": 0, "rata_rata_kelas": 0, "persentase_lulus": 0, "detail": []}

    siswa_unik = set(n["nis"] for n in nilai_list)
    total = sum(n["nilai_akhir"] for n in nilai_list)
    jumlah = len(nilai_list)
    lulus = sum(1 for n in nilai_list if n["status"] == "Lulus")

    return {
        "kelas": kelas,
        "jumlah_siswa": len(siswa_unik),
        "rata_rata_kelas": round(total / jumlah, 2),
        "persentase_lulus": round((lulus / jumlah) * 100, 2),
        "detail": nilai_list
    }
```

---

## Dependency Injection & Auth Flow

### `core/dependencies.py`
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import decode_token

security = HTTPBearer()

def get_db():
    """Dependency: inject database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency: extract current user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
```

### Role Guard
Setiap router endpoint menggunakan check role manual:
```python
if current_user.role not in ["admin", "guru"]:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
```

---

## Seed Data (opsional, untuk testing)
Saat aplikasi pertama kali dijalankan, buat data awal:
- 1 user Admin: `admin` / `admin123`
- 2 user Guru: `guru1` / `guru123`, `guru2` / `guru123`
- 3 user Siswa: `siswa1` / `siswa123`, `siswa2` / `siswa123`, `siswa3` / `siswa123`

---

## Urutan Implementasi

| No | Langkah | File |
|----|---------|------|
| 1 | Inisialisasi project & virtual env | `requirements.txt` |
| 2 | Konfigurasi database | `core/database.py`, `app/config.py` |
| 3 | Security (JWT + hashing) | `core/security.py` |
| 4 | Dependencies (DB session + auth guard) | `core/dependencies.py`, `core/exceptions.py` |
| 5 | Auth module | `features/auth/models.py` → `schemas.py` → `service.py` → `router.py` |
| 6 | Siswa module | `features/siswa/models.py` → `schemas.py` → `repository.py` → `service.py` → `router.py` |
| 7 | Guru module | `features/guru/` (sama seperti siswa) |
| 8 | Nilai module + utils | `features/nilai/utils.py` → `models.py` → `repository.py` → `service.py` → `router.py` |
| 9 | Laporan module | `features/laporan/service.py` → `router.py` |
| 10 | Entry point | `app/main.py` — gabungkan semua router |
| 11 | Seed data | Script seed atau endpoint khusus |
| 12 | Testing | Jalankan server, test via Swagger UI (`/docs`) |

---

## Menjalankan Server

```bash
cd sistem_sekolah_py
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Buka `http://localhost:8000/docs` untuk Swagger UI.
