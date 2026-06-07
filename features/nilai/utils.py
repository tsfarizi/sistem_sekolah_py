from features.nilai.models import Nilai


def validasi_nilai(nilai: float) -> bool:
    return 0.0 <= nilai <= 100.0


def hitung_nilai_akhir(tugas: float, uts: float, uas: float) -> float:
    return round(0.3 * tugas + 0.3 * uts + 0.4 * uas, 2)


def tentukan_status(nilai_akhir: float) -> str:
    return "Lulus" if nilai_akhir >= 70.0 else "Tidak Lulus"


def nilai_to_dict(n: Nilai) -> dict:
    return {
        "id": n.id,
        "nis": n.nis,
        "guru_mengajar_id": n.guru_mengajar_id,
        "tugas": n.tugas,
        "uts": n.uts,
        "uas": n.uas,
        "nilai_akhir": n.nilai_akhir,
        "status": n.status,
        "created_at": n.created_at,
        "updated_at": n.updated_at,
    }


def generate_laporan_siswa(nilai_list: list[dict]) -> dict:
    if not nilai_list:
        return {"rata_rata": 0, "jumlah_matapelajaran": 0, "lulus": 0, "tidak_lulus": 0, "status_akhir": "Tidak Lulus", "detail": []}

    total = sum(n["nilai_akhir"] for n in nilai_list)
    jumlah = len(nilai_list)
    lulus = sum(1 for n in nilai_list if n["status"] == "Lulus")
    tidak_lulus = jumlah - lulus

    return {
        "rata_rata": round(total / jumlah, 2),
        "jumlah_matapelajaran": jumlah,
        "lulus": lulus,
        "tidak_lulus": tidak_lulus,
        "status_akhir": "Lulus" if tidak_lulus == 0 else "Tidak Lulus",
        "detail": nilai_list
    }


def generate_laporan_kelas(nilai_list: list[dict], kelas_id: int, kelas_nama: str) -> dict:
    if not nilai_list:
        return {"kelas_id": kelas_id, "kelas_nama": kelas_nama, "jumlah_siswa": 0, "rata_rata_kelas": 0, "persentase_lulus": 0, "detail": []}

    siswa_unik = set(n["nis"] for n in nilai_list)
    total = sum(n["nilai_akhir"] for n in nilai_list)
    jumlah = len(nilai_list)
    lulus = sum(1 for n in nilai_list if n["status"] == "Lulus")

    return {
        "kelas_id": kelas_id,
        "kelas_nama": kelas_nama,
        "jumlah_siswa": len(siswa_unik),
        "rata_rata_kelas": round(total / jumlah, 2),
        "persentase_lulus": round((lulus / jumlah) * 100, 2),
        "detail": nilai_list
    }
