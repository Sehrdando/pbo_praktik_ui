import customtkinter as ctk

from models import FILE_KENDARAAN, RepositoriKendaraan
from ui import (BG_INPUT, BORDER, CYAN, MUTED, TEXT, LatarBergerak, buat_header, buat_kartu, buat_label_total,
                buat_tombol, buat_treeview, efek_fokus, fnt, hitung_naik, isi_tabel, siapkan_window, toast)

repo = RepositoriKendaraan()
state = {"data": [], "mtime": 0}


def tampilkan_kendaraan(animasi=True):
    """Baca CSV, terapkan pencarian, isi tabel, dan hitung total."""
    state["data"] = repo.semua()
    cari = entry_cari.get().strip().lower()
    hasil = [k for k in state["data"] if not cari or cari in " ".join(map(str, k.to_list())).lower()]
    isi_tabel(tree, hasil, animasi)
    hitung_naik(label_total, len(hasil), "🚗 Total Kendaraan: {}")
    state["mtime"] = FILE_KENDARAAN.stat().st_mtime if FILE_KENDARAAN.exists() else 0


def cek_perubahan():
    """Otomatis muat ulang saat kendaraan.csv berubah (mis. setelah tambah data)."""
    mtime = FILE_KENDARAAN.stat().st_mtime if FILE_KENDARAAN.exists() else 0
    if mtime != state["mtime"]:
        tampilkan_kendaraan()
        toast(root, "Data diperbarui otomatis", CYAN)
    root.after(1500, cek_perubahan)


root = ctk.CTk()
siapkan_window(root, "Daftar Kendaraan", 980, 640)
latar = LatarBergerak(root)
latar.pack(fill="both", expand=True)

buat_header(latar, "DAFTAR KENDARAAN", "#1F9D8B")

# --- pencarian langsung ---
toolbar = buat_kartu(latar)
toolbar.pack(fill="x", padx=25, pady=(16, 10))
ctk.CTkLabel(toolbar, text="🔍 Cari:", text_color=MUTED, font=fnt(12, True)).pack(side="left", padx=(16, 8), pady=10)
entry_cari = ctk.CTkEntry(toolbar, placeholder_text="ID, merek, model, atau plat…", width=380, height=36, corner_radius=10,
                          fg_color=BG_INPUT, border_color=BORDER, text_color=TEXT, font=fnt(13))
entry_cari.pack(side="left", pady=10)
efek_fokus(entry_cari)
entry_cari.bind("<KeyRelease>", lambda e: tampilkan_kendaraan(animasi=False))

# --- tabel ---
tabel = buat_kartu(latar)
tabel.pack(fill="both", expand=True, padx=25)
tree = buat_treeview(tabel)

# --- footer ---
footer = buat_kartu(latar)
footer.pack(fill="x", padx=25, pady=(10, 16))
label_total = buat_label_total(footer)
buat_tombol(footer, "Keluar", root.destroy, "#C94F5D", width=12, side="right")
buat_tombol(footer, "Refresh Data", tampilkan_kendaraan, "#1F9D8B", width=15, side="right")

tampilkan_kendaraan()
root.after(1500, cek_perubahan)
root.mainloop()
