import csv
from datetime import date
from pathlib import Path

FOLDER_PROYEK = Path(__file__).resolve().parent
FILE_KENDARAAN = FOLDER_PROYEK / "kendaraan.csv"
HEADER_KENDARAAN = ["ID Kendaraan", "Merek", "Model", "Tahun", "Plat Nomor", "Status"]


class Kendaraan:
    def __init__(self, id_kendaraan, merk, model, tahun, plat_nomor, status="Tersedia"):
        self.id_kendaraan = id_kendaraan
        self.merk = merk
        self.model = model
        self.tahun = tahun
        self.plat_nomor = plat_nomor
        self.status = status

    def validasi(self):
        """Cek isian; lempar ValueError berisi pesan yang mudah dibaca."""
        for nama, nilai in (("ID Kendaraan", self.id_kendaraan), ("Merek", self.merk), ("Model", self.model),
                            ("Tahun", self.tahun), ("Plat Nomor", self.plat_nomor)):
            if not str(nilai).strip():
                raise ValueError(f"{nama} wajib diisi.")
        if not str(self.tahun).isdigit() or not 1950 <= int(self.tahun) <= date.today().year + 1:
            raise ValueError("Tahun harus berupa angka yang masuk akal (1950 - sekarang).")
        self.plat_nomor = " ".join(str(self.plat_nomor).upper().split())

    def to_list(self):
        return [self.id_kendaraan, self.merk, self.model, self.tahun, self.plat_nomor, self.status]

    def __str__(self):
        return f"{self.id_kendaraan} | {self.merk} {self.model} ({self.tahun}) | Plat: {self.plat_nomor} | {self.status}"


class Pelanggan:
    def __init__(self, id_pelanggan, nama, no_hp):
        self.id_pelanggan = id_pelanggan
        self.nama = nama
        self.no_hp = no_hp

    def to_list(self):
        return [self.id_pelanggan, self.nama, self.no_hp]

    def __str__(self):
        return f"{self.nama} ({self.id_pelanggan}) - No. HP {self.no_hp}"


class RepositoriKendaraan:
    """Baca/tulis data kendaraan ke kendaraan.csv."""

    def __init__(self, path=FILE_KENDARAAN):
        self.path = Path(path)

    def semua(self):
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []
        with self.path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)  # lewati header
            return [Kendaraan(*[c.strip() for c in row[:6]]) for row in reader if len(row) >= 5]

    def tambah(self, kendaraan):
        kendaraan.validasi()
        for k in self.semua():
            if k.id_kendaraan == kendaraan.id_kendaraan:
                raise ValueError("ID Kendaraan sudah dipakai.")
            if " ".join(k.plat_nomor.upper().split()) == kendaraan.plat_nomor:
                raise ValueError("Plat nomor sudah terdaftar.")
        file_baru = not self.path.exists() or self.path.stat().st_size == 0
        with self.path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file_baru:
                writer.writerow(HEADER_KENDARAAN)
            writer.writerow(kendaraan.to_list())
