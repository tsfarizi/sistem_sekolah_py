from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.database import SessionLocal, init_db
from core.security import hash_password
from core.exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
)
from features.auth.models import User

from features.auth.router import router as auth_router, user_router
from features.siswa.router import router as siswa_router
from features.guru.router import router as guru_router
from features.nilai.router import router as nilai_router
from features.laporan.router import router as laporan_router
from features.mata_pelajaran.router import router as matapelajaran_router
from features.kelas.router import router as kelas_router
from features.guru_mengajar.router import router as guru_mengajar_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        db = SessionLocal()
        try:
            if db.query(User).count() == 0:
                admin_user = User(
                    username="admin",
                    password_hash=hash_password("admin123"),
                    role="admin",
                    nama="Administrator",
                )
                db.add(admin_user)
                db.commit()
        finally:
            db.close()
    except Exception:
        pass
    yield


app = FastAPI(
    title="Sistem Pengolahan Nilai Siswa API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400, content={"detail": exc.detail})


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"detail": exc.detail})


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(status_code=403, content={"detail": exc.detail})


@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(status_code=409, content={"detail": exc.detail})


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(siswa_router)
app.include_router(guru_router)
app.include_router(nilai_router)
app.include_router(laporan_router)
app.include_router(matapelajaran_router)
app.include_router(kelas_router)
app.include_router(guru_mengajar_router)
