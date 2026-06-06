from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from features.siswa.models import Siswa
from features.nilai.models import Nilai
from features.guru_mengajar.models import GuruMengajar
from features.nilai.utils import generate_laporan_siswa, generate_laporan_kelas


def laporan_by_kelas(db: Session, kelas_id: int | None = None) -> list[dict]:
    query = db.query(Nilai).join(Nilai.guru_mengajar)
    if kelas_id:
        query = query.filter(GuruMengajar.kelas_id == kelas_id)
    nilai_list = query.all()
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
        nilai_dicts = [n.to_dict() for n in k_data["items"]]
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


def laporan_by_siswa(db: Session, nis: str) -> dict:
    siswa = db.query(Siswa).filter(Siswa.nis == nis).first()
    if not siswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Siswa tidak ditemukan"
        )
    nilai_list = db.query(Nilai).filter(Nilai.nis == nis).all()
    nilai_dicts = [n.to_dict() for n in nilai_list]
    ringkasan = generate_laporan_siswa(nilai_dicts)
    ringkasan.pop("detail", None)
    return {
        "siswa": siswa,
        "nilai_list": nilai_list,
        "ringkasan": ringkasan,
    }
