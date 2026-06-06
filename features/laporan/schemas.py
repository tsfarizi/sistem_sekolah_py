from pydantic import BaseModel
from features.siswa.schemas import SiswaResponse
from features.nilai.schemas import NilaiResponse


class RingkasanSiswa(BaseModel):
    rata_rata: float
    jumlah_mapel: int
    lulus: int
    tidak_lulus: int
    status_akhir: str


class LaporanSiswaResponse(BaseModel):
    siswa: SiswaResponse
    nilai_list: list[NilaiResponse]
    ringkasan: RingkasanSiswa


class DetailKelas(BaseModel):
    nis: str
    nama: str
    rata_rata: float
    jumlah_lulus: int
    jumlah_tidak_lulus: int
    status: str


class LaporanKelasResponse(BaseModel):
    kelas_id: int
    kelas_nama: str
    jumlah_siswa: int
    rata_rata_kelas: float
    persentase_lulus: float
    detail: list[DetailKelas]
