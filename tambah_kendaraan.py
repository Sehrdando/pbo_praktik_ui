import customtkinter as ctk

from models import Kendaraan, RepositoriKendaraan
from ui import (GREEN, RED, LatarBergerak, BG_CARD, buat_entry, buat_form, buat_header, buat_tombol, fnt, kilau,
                shake, siapkan_window, toast)

repo = RepositoriKendaraan()


def simpan_kendaraan(entries):
    id_k, merk, model, tahun, plat = [e.get().strip() for e in entries]
    try:
        repo.tambah(Kendaraan(id_k, merk, model, tahun, plat))
    except ValueError as err:
        pesan.configure(text="⚠  " + str(err))
        toast(root, str(err), RED)
        shake(root)
        return
    pesan.configure(text="")
    toast(root, "Kendaraan berhasil disimpan")
    kilau(form, GREEN)
    for e in entries:
        e.delete(0, "end")
    entries[0].focus()


# ==================================
# WINDOW + LATAR BERGERAK
# ==================================
root = ctk.CTk()
siapkan_window(root, "Tambah Kendaraan", 700, 660)
latar = LatarBergerak(root)
latar.pack(fill="both", expand=True)

buat_header(latar, "TAMBAH DATA KENDARAAN", "#2878FF")
form = buat_form(latar)

entries = [buat_entry(form, label) for label in ("ID Kendaraan", "Merek", "Model", "Tahun", "Plat Nomor")]

# Enter = pindah ke kolom berikutnya; Enter di kolom terakhir = simpan
for i, e in enumerate(entries):
    e.bind("<Return>", lambda ev, i=i: entries[i + 1].focus() if i + 1 < len(entries) else simpan_kendaraan(entries))

pesan = ctk.CTkLabel(form, text="", text_color=RED, font=fnt(12, True), anchor="w")
pesan.pack(fill="x", padx=28, pady=(2, 0))

frm = ctk.CTkFrame(form, fg_color="transparent")
frm.pack(fill="x", padx=23, pady=(10, 18))

buat_tombol(frm, "💾 Simpan Kendaraan", lambda: simpan_kendaraan(entries), "#2878FF", width=18, side="left")
buat_tombol(frm, "❌ Keluar", root.destroy, "#C94F5D", width=12, side="right")

entries[0].focus()
root.mainloop()
