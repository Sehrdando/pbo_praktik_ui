import subprocess
import sys
from datetime import datetime

import customtkinter as ctk

from models import FOLDER_PROYEK, RepositoriKendaraan
from ui import (BG_APP, BG_CARD, BLUE, BORDER, CYAN, GREEN, MUTED, YELLOW, LatarBergerak, Speedometer, buat_header,
                buat_kartu, buat_kartu_stat, buat_menu_button, denyut, fnt, hitung_naik, siapkan_window)

repo = RepositoriKendaraan()


def buka_modul(nama_file):
    subprocess.Popen([sys.executable, str(FOLDER_PROYEK / nama_file)], cwd=FOLDER_PROYEK)


def buka_tambah_kendaraan():
    buka_modul("tambah_kendaraan.py")


def buka_tampil_kendaraan():
    buka_modul("tampil_kendaraan.py")


def keluar(root):
    root.destroy()


# ==================================
# WINDOW + LATAR BERGERAK (semua isi ada di dalam `latar`)
# ==================================
root = ctk.CTk()
siapkan_window(root, "APEX GARAGE", 720, 790)
latar = LatarBergerak(root)
latar.pack(fill="both", expand=True)

buat_header(latar, "APEX GARAGE", BLUE, 110, "Precision Service. Premium Care.")

# ==================================
# PANEL DASHBOARD: speedometer + kartu statistik
# ==================================
dash = buat_kartu(latar)
dash.pack(fill="x", padx=40, pady=(18, 14))
gauge = Speedometer(dash, ukuran=280, satuan="KENDARAAN TERDAFTAR")
gauge.pack(side="left", padx=(16, 8), pady=14)
kolom = ctk.CTkFrame(dash, fg_color="transparent")
kolom.pack(side="left", fill="both", expand=True, padx=(8, 18), pady=14)

kartu = {}
for kunci, judul, warna in (("total", "Total Kendaraan", CYAN), ("tersedia", "Tersedia", GREEN), ("servis", "Dalam Servis", YELLOW)):
    k, nilai = buat_kartu_stat(kolom, judul, warna)
    k.pack(fill="both", expand=True, pady=5)
    kartu[kunci] = nilai


def perbarui_statistik():
    data = repo.semua()
    angka = {"total": len(data), "tersedia": sum(k.status == "Tersedia" for k in data),
             "servis": sum(k.status == "Dalam Servis" for k in data)}
    for kunci, nilai in angka.items():
        if getattr(kartu[kunci], "_n", None) != nilai:  # animasi hanya saat angka berubah
            hitung_naik(kartu[kunci], nilai)
    gauge.set(angka["total"])
    root.after(2000, perbarui_statistik)


# ==================================
# MENU
# ==================================
buat_menu_button(latar, "🚗  Tambah Kendaraan", buka_tambah_kendaraan, "#2878FF").pack(fill="x", padx=40, pady=7)
buat_menu_button(latar, "📋  Tampilkan Kendaraan", buka_tampil_kendaraan, "#1F9D8B").pack(fill="x", padx=40, pady=7)
buat_menu_button(latar, "🚪  Keluar", lambda: keluar(root), "#C94F5D").pack(fill="x", padx=40, pady=7)

# ==================================
# FOOTER: status online berdenyut + jam
# ==================================
footer = buat_kartu(latar)
footer.pack(fill="x", padx=40, pady=(10, 16), side="bottom")
status = ctk.CTkLabel(footer, text="●  SISTEM ONLINE", text_color=GREEN, font=fnt(11, True))
status.pack(side="left", padx=16, pady=9)
jam = ctk.CTkLabel(footer, text="", text_color=MUTED, font=fnt(11))
jam.pack(side="right", padx=16)
denyut(status, GREEN)


def tick():
    jam.configure(text=datetime.now().strftime("%d %b %Y  ·  %H:%M:%S"))
    root.after(1000, tick)


tick()
perbarui_statistik()
root.mainloop()
