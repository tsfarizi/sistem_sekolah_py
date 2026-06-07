from sqlalchemy.orm import Session
from core.dependencies import CurrentUser
from core.exceptions import NotFoundException, ForbiddenException
from features.laporan.repository import (
    get_nilai_joined,
    get_nilai_by_nis,
    get_siswa_by_nis,
    get_kelas_ids_by_guru,
    nilai_list_to_dicts,
)
from features.nilai.utils import generate_laporan_siswa, generate_laporan_kelas


def laporan_by_kelas(db: Session, kelas_id: int | None = None, current_user: CurrentUser | None = None) -> list[dict]:
    kelas_ids = None
    if current_user and current_user.role == "guru":
        if not current_user.guru:
            return []
        kelas_ids = get_kelas_ids_by_guru(db, current_user.guru.id)
        if not kelas_ids:
            return []
    nilai_list = get_nilai_joined(db, kelas_id=kelas_id, kelas_ids=kelas_ids)
    kelas_map: dict[int, dict] = {}
    for n in nilai_list:
        if n.guru_mengajar and n.guru_mengajar.kelas:
            k_id = n.guru_mengajar.kelas.id
            k_nama = n.guru_mengajar.kelas.nama
        else:
            continue
        if k_id not in kelas_map:
            kelas_map[k_id] = {"nama": k_nama, "items": []}
        kelas_map[k_id]["items"].append(n)
    result = []
    for k_id, k_data in kelas_map.items():
        k_nama = k_data["nama"]
        nilai_dicts = nilai_list_to_dicts(k_data["items"])
        kelas_stats = generate_laporan_kelas(nilai_dicts, k_id, k_nama)

        siswa_map: dict[str, dict] = {}
        for n in k_data["items"]:
            nis = n.nis
            if nis not in siswa_map:
                siswa_map[nis] = {
                    "nis": nis,
                    "nama": n.siswa.nama if n.siswa else "",
                    "nilai_list": [],
                }
            siswa_map[nis]["nilai_list"].append(n)
        summary_items = []
        for nis, sdata in siswa_map.items():
            nilai_siswa = sdata["nilai_list"]
            total_nilai_siswa = sum(n.nilai_akhir for n in nilai_siswa)
            jumlah = len(nilai_siswa)
            lulus_count = sum(1 for n in nilai_siswa if n.status == "Lulus")
            tidak_lulus_count = jumlah - lulus_count
            rata = round(total_nilai_siswa / jumlah, 2) if jumlah > 0 else 0.0
            status_siswa = "Lulus" if tidak_lulus_count == 0 else "Tidak Lulus"
            summary_items.append({
                "nis": nis,
                "nama": sdata["nama"],
                "rata_rata": rata,
                "jumlah_lulus": lulus_count,
                "jumlah_tidak_lulus": tidak_lulus_count,
                "status": status_siswa,
            })
        result.append({
            "kelas_id": kelas_stats["kelas_id"],
            "kelas_nama": kelas_stats["kelas_nama"],
            "jumlah_siswa": kelas_stats["jumlah_siswa"],
            "rata_rata_kelas": kelas_stats["rata_rata_kelas"],
            "persentase_lulus": kelas_stats["persentase_lulus"],
            "detail": summary_items,
        })
    return result


def laporan_by_siswa(db: Session, nis: str, current_user: CurrentUser | None = None) -> dict:
    siswa = get_siswa_by_nis(db, nis)
    if not siswa:
        raise NotFoundException("Siswa tidak ditemukan")
    if current_user and current_user.role == "guru":
        if not current_user.guru:
            raise ForbiddenException("Akun guru tidak valid")
        guru_kelas_ids = get_kelas_ids_by_guru(db, current_user.guru.id)
        if siswa.kelas_id not in guru_kelas_ids:
            raise ForbiddenException("Anda tidak memiliki akses ke laporan siswa ini")
    nilai_list = get_nilai_by_nis(db, nis)
    nilai_dicts = nilai_list_to_dicts(nilai_list)
    ringkasan = generate_laporan_siswa(nilai_dicts)
    ringkasan.pop("detail", None)
    return {
        "siswa": siswa,
        "nilai_list": nilai_list,
        "ringkasan": ringkasan,
    }
