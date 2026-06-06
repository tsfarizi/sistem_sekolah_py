from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from app.config import JWT_SECRET
from core.database import engine, Base, SessionLocal
from core.security import hash_password
from features.auth.models import User

from features.auth.router import router as auth_router, user_router
from features.siswa.router import router as siswa_router
from features.guru.router import router as guru_router
from features.nilai.router import router as nilai_router
from features.laporan.router import router as laporan_router
from features.mata_pelajaran.router import router as mapel_router
from features.kelas.router import router as kelas_router
from features.guru_mengajar.router import router as guru_mengajar_router

from app.admin import AdminAuth, UserAdmin, NilaiAdmin, MataPelajaranAdmin, KelasAdmin, GuruMengajarAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(siswa_router)
app.include_router(guru_router)
app.include_router(nilai_router)
app.include_router(laporan_router)
app.include_router(mapel_router)
app.include_router(kelas_router)
app.include_router(guru_mengajar_router)

auth_backend = AdminAuth(secret_key=JWT_SECRET)
admin = Admin(app, engine, authentication_backend=auth_backend)

admin.add_view(UserAdmin)
admin.add_view(NilaiAdmin)
admin.add_view(MataPelajaranAdmin)
admin.add_view(KelasAdmin)
admin.add_view(GuruMengajarAdmin)
