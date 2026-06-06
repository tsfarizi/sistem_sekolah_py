def validasi_nilai(nilai: float) -> bool:
    return 0.0 <= nilai <= 100.0


def hitung_nilai_akhir(tugas: float, uts: float, uas: float) -> float:
    return round(0.3 * tugas + 0.3 * uts + 0.4 * uas, 2)


def tentukan_status(nilai_akhir: float) -> str:
    return "Lulus" if nilai_akhir >= 70.0 else "Tidak Lulus"


def generate_laporan_siswa(nilai_list: list[dict]) -> dict:
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
