from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from wtforms import PasswordField
from core.database import SessionLocal
from core.security import hash_password, verify_password
from features.auth.models import User
from features.siswa.models import Siswa
from features.guru.models import Guru
from features.nilai.models import Nilai
from features.mata_pelajaran.models import MataPelajaran
from features.kelas.models import Kelas
from features.guru_mengajar.models import GuruMengajar


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))
        db = SessionLocal()
        try:
            user = db.query(User).filter(
                User.username == username, User.role == "admin"
            ).first()
            if not user or not verify_password(password, user.password_hash):
                return False
            request.session.update({"admin_user_id": user.id})
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_user_id = request.session.get("admin_user_id")
        if not admin_user_id:
            return False
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == admin_user_id, User.role == "admin").first()
            return user is not None
        finally:
            db.close()


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role, User.nama, User.created_at]
    column_searchable_list = [User.username, User.nama, User.role]
    column_sortable_list = [User.id, User.username, User.role, User.nama, User.created_at]
    form_excluded_columns = [User.password_hash, User.siswa, User.guru]
    form_extra_fields = {
        "password": PasswordField("Password"),
    }
    can_create = True
    can_edit = True
    can_delete = True
    name = "User"
    name_plural = "Users"

    async def on_model_change(self, data: dict, model, is_created: bool, request: Request):
        password = data.pop("password", None)
        if password:
            model.password_hash = hash_password(password)
        return await super().on_model_change(data, model, is_created, request)


class SiswaAdmin(ModelView, model=Siswa):
    column_list = [Siswa.nis, Siswa.nama, Siswa.kelas_id, Siswa.user_id]
    column_searchable_list = [Siswa.nis, Siswa.nama]
    column_sortable_list = [Siswa.nis, Siswa.nama, Siswa.kelas_id]
    form_excluded_columns = [Siswa.nilai_list, Siswa.kelas, Siswa.user]
    name = "Siswa"
    name_plural = "Siswa"


class GuruAdmin(ModelView, model=Guru):
    column_list = [Guru.id, Guru.nama, Guru.user_id]
    column_searchable_list = [Guru.id, Guru.nama]
    column_sortable_list = [Guru.id, Guru.nama]
    form_excluded_columns = [Guru.mengajar_list, Guru.wali_kelas_list, Guru.user]
    name = "Guru"
    name_plural = "Guru"


class NilaiAdmin(ModelView, model=Nilai):
    column_list = [
        Nilai.id, Nilai.nis, Nilai.guru_mengajar_id,
        Nilai.tugas, Nilai.uts, Nilai.uas, Nilai.nilai_akhir, Nilai.status,
        Nilai.created_at, Nilai.updated_at,
    ]
    column_searchable_list = [Nilai.nis]
    column_sortable_list = [Nilai.id, Nilai.nis, Nilai.nilai_akhir, Nilai.status]
    form_excluded_columns = [Nilai.nilai_akhir, Nilai.status, Nilai.siswa, Nilai.guru_mengajar]
    name = "Nilai"
    name_plural = "Nilai"


class MataPelajaranAdmin(ModelView, model=MataPelajaran):
    column_list = [MataPelajaran.id, MataPelajaran.nama]
    column_searchable_list = [MataPelajaran.nama]
    column_sortable_list = [MataPelajaran.id, MataPelajaran.nama]
    form_excluded_columns = [MataPelajaran.mengajar_list]
    name = "Mata Pelajaran"
    name_plural = "Mata Pelajaran"


class KelasAdmin(ModelView, model=Kelas):
    column_list = [Kelas.id, Kelas.nama, Kelas.wali_kelas_id]
    column_searchable_list = [Kelas.nama]
    column_sortable_list = [Kelas.id, Kelas.nama]
    form_excluded_columns = [Kelas.wali_kelas, Kelas.siswa_list, Kelas.mengajar_list]
    name = "Kelas"
    name_plural = "Kelas"


class GuruMengajarAdmin(ModelView, model=GuruMengajar):
    column_list = [GuruMengajar.id, GuruMengajar.guru_id, GuruMengajar.kelas_id, GuruMengajar.mata_pelajaran_id]
    column_searchable_list = [GuruMengajar.guru_id]
    column_sortable_list = [GuruMengajar.id, GuruMengajar.guru_id, GuruMengajar.kelas_id, GuruMengajar.mata_pelajaran_id]
    form_excluded_columns = [GuruMengajar.guru, GuruMengajar.kelas, GuruMengajar.mata_pelajaran, GuruMengajar.nilai_list]
    name = "Guru Mengajar"
    name_plural = "Guru Mengajar"
