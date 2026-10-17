import math
import random
import tkinter as tk
from tkinter import ttk, font as tkfont

import customtkinter as ctk

# ==========================================
# PALET WARNA (tema gelap APEX GARAGE)
# ==========================================
BG_APP = "#0A101A"
BG_CARD = "#111C2B"
BG_INPUT = "#0D1522"
TEXT = "#F3F7FC"
MUTED = "#9BAEC4"
BORDER = "#26364B"
CYAN, BLUE, GREEN = "#42D9F5", "#2878FF", "#2DD4A7"
YELLOW, RED, PURPLE = "#F6BE4F", "#FF6878", "#A78BFA"
HEADER_COLOR = BLUE
GRAD = (CYAN, "#7DA8FF", PURPLE)
FONT = "Segoe UI"


def fnt(size=12, bold=False):
    return ctk.CTkFont(family=FONT, size=size, weight="bold" if bold else "normal")


# ==========================================
# EFEK: dasar animasi
# ==========================================
def lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    t = max(0.0, min(1.0, t))
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def grad_color(stops, t):
    n = len(stops) - 1
    s = max(0.0, min(0.9999, t)) * n
    i = int(s)
    return lerp(stops[i], stops[i + 1], s - i)


def animate(widget, fn, steps=16, delay=16):
    """Panggil fn(p) dengan p 0→1 (ease-out). Aman bila widget sudah ditutup."""
    def go(i):
        try:
            fn(1 - (1 - i / steps) ** 3)
            if i < steps:
                widget.after(delay, lambda: go(i + 1))
        except Exception:
            pass
    go(0)


def siapkan_window(root, judul, lebar, tinggi):
    """Tema gelap CustomTkinter, ukuran, posisi tengah layar, dan fade-in."""
    ctk.set_appearance_mode("dark")
    root.title(judul)
    root.configure(fg_color=BG_APP)
    skala = root._get_window_scaling() if hasattr(root, "_get_window_scaling") else 1
    root.geometry(f"{lebar}x{tinggi}")
    tk.Wm.geometry(root, f"+{int((root.winfo_screenwidth() - lebar * skala) // 2)}+{int((root.winfo_screenheight() - tinggi * skala) // 2 - 20)}")
    try:
        root.attributes("-alpha", 0)
        animate(root, lambda p: root.attributes("-alpha", p), 14)
    except tk.TclError:
        pass


def shake(win):
    """Getarkan jendela (dipakai saat input salah)."""
    try:
        x, y = win.winfo_x(), win.winfo_y()
    except tk.TclError:
        return
    for i, dx in enumerate((-12, 12, -9, 9, -5, 5, 0)):
        win.after(i * 28, lambda dx=dx: tk.Wm.geometry(win, f"+{x + dx}+{y}"))


def kilau(widget, warna):
    """Border widget menyala lalu meredup."""
    animate(widget, lambda p: widget.configure(border_color=lerp(warna, BORDER, p)), 24)


def hitung_naik(label, n, format_teks="{}"):
    """Angka pada label berhitung naik dari nilai sebelumnya ke n."""
    awal = getattr(label, "_n", 0)
    label._n = n
    animate(label, lambda p: label.configure(text=format_teks.format(int(awal + (n - awal) * p))), 22)


def denyut(label, warna, t=0):
    """Warna teks label berdenyut terus-menerus."""
    try:
        label.configure(text_color=lerp(BG_APP, warna, .45 + .55 * abs(((t % 40) - 20) / 20)))
        label.after(60, lambda: denyut(label, warna, t + 1))
    except Exception:
        pass


def toast(win, teks, warna=GREEN):
    """Notifikasi kecil yang naik dari bawah lalu hilang sendiri."""
    f = ctk.CTkFrame(win, fg_color="#162438", corner_radius=12, border_width=1, border_color=warna)
    ctk.CTkLabel(f, text="●  " + teks, font=fnt(12, True), text_color=TEXT).pack(padx=20, pady=11)
    ys = list(range(40, -26, -5))

    def go(i, d):
        try:
            if i < 0 or i >= len(ys):
                if d < 0:
                    f.destroy()
                else:
                    f.after(1800, lambda: go(len(ys) - 1, -1))
                return
            f.place(relx=.5, rely=1.0, anchor="s", y=ys[i])
            f.lift()
            f.after(14, lambda: go(i + d, d))
        except Exception:
            pass
    go(0, 1)


# ==========================================
# LATAR BERGERAK (bola cahaya melayang + garis kecepatan)
# Semua isi halaman dibuat DI DALAM canvas ini.
# ==========================================
class LatarBergerak(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_APP, highlightthickness=0, bd=0)
        self.t = 0
        tint = (BLUE, CYAN, PURPLE, BLUE, CYAN)
        self.orbs = [[random.uniform(0, 6.28), random.uniform(0, 6.28), random.uniform(.010, .022),
                      random.uniform(.008, .018), random.randint(100, 180), c] for c in tint]
        self.streaks = [[random.random(), random.random(), random.uniform(.004, .012), random.randint(40, 120)] for _ in range(14)]
        self.after(30, self._frame)

    def _frame(self):
        try:
            if not self.winfo_exists():
                return
            w, h, t = self.winfo_width(), self.winfo_height(), self.t
            self.delete("bg")
            if w > 50:
                for o in self.orbs:
                    x = w * (.5 + .42 * math.sin(t * o[2] + o[0]))
                    y = h * (.5 + .42 * math.cos(t * o[3] + o[1]))
                    for k in range(5):  # lingkaran bertumpuk = efek glow
                        r = o[4] * (1 - k / 5)
                        self.create_oval(x - r, y - r, x + r, y + r, fill=lerp(BG_APP, o[5], .02 + .04 * k), outline="", tags="bg")
                for s in self.streaks:
                    s[0] = (s[0] + s[2]) % 1.15
                    x, y = s[0] * w - s[3], s[1] * h
                    self.create_line(x, y, x + s[3], y, fill=lerp(BG_APP, CYAN, .3), tags="bg")
            self.t += 1
            self.after(33, self._frame)
        except tk.TclError:
            pass


# ==========================================
# SPEEDOMETER ala dashboard mobil
# ==========================================
class Speedometer(tk.Canvas):
    """Jarum menyapu penuh saat start (seperti mobil dinyalakan), lalu menunjuk nilai dan bergetar halus."""
    def __init__(self, parent, ukuran=280, satuan="KENDARAAN", bg=BG_CARD):
        super().__init__(parent, width=ukuran, height=ukuran, bg=bg, highlightthickness=0, bd=0)
        self.u, self.satuan, self.bg = ukuran, satuan, bg
        self.maks, self.target, self.v, self.fase, self.t = 10, 0, 0.0, 0, 0
        self.after(30, self._frame)

    def set(self, nilai):
        self.target = nilai
        self.maks = max(10, int(math.ceil(nilai / 10.0)) * 10)

    def _frame(self):
        try:
            if not self.winfo_exists():
                return
            goal = self.maks if self.fase == 0 else self.target
            self.v += (goal - self.v) * (.07 if self.fase == 0 else .1)
            if self.fase == 0 and self.v >= self.maks * .97:
                self.fase = 1
            getar = (math.sin(self.t * 1.9) * .004 + random.uniform(-.0025, .0025)) * self.maks if self.fase else 0
            self._draw(self.v + getar)
            self.t += 1
            self.after(33, self._frame)
        except tk.TclError:
            pass

    def _draw(self, nilai):
        self.delete("all")
        u = self.u
        c, R = u / 2, u * .44
        f = max(0.0, min(1.0, nilai / self.maks))
        pt = lambda r, frac: (c + r * math.cos(math.radians(225 - 270 * frac)), c - r * math.sin(math.radians(225 - 270 * frac)))
        for k in range(5):  # cahaya luar
            r = R + 16 - k * 3
            self.create_oval(c - r, c - r, c + r, c + r, outline=lerp(self.bg, CYAN, .05 + .07 * k), width=2)
        self.create_oval(c - R, c - R, c + R, c + R, fill=BG_INPUT, outline="#1B2D4A", width=3)
        box = (c - R + 14, c - R + 14, c + R - 14, c + R - 14)
        self.create_arc(*box, start=225, extent=-270, style="arc", outline="#1B2D4A", width=8)
        self.create_arc(*box, start=225 - 270 * .8, extent=-270 * .2, style="arc", outline="#4A2330", width=8)  # zona merah
        for i in range(int(270 * f / 5) + 1):  # busur nilai bergradien cyan → kuning → merah
            self.create_arc(*box, start=225 - 5 * i, extent=-5.6, style="arc",
                            outline=grad_color((CYAN, "#7DA8FF", YELLOW, RED), 5 * i / 270), width=8)
        for i in range(51):  # garis skala + angka
            fr, besar = i / 50, i % 5 == 0
            merah = fr >= .8
            x1, y1 = pt(R - (34 if besar else 28), fr)
            x2, y2 = pt(R - 22, fr)
            self.create_line(x1, y1, x2, y2, fill=RED if merah else (TEXT if besar else "#5B7BA6"), width=2 if besar else 1)
            if besar:
                tx, ty = pt(R - 48, fr)
                self.create_text(tx, ty, text=str(round(self.maks * fr)), font=(FONT, 8, "bold"), fill=RED if merah else MUTED)
        # jarum
        a = math.radians(225 - 270 * f)
        tip = (c + (R - 20) * math.cos(a), c - (R - 20) * math.sin(a))
        nx, ny = -math.sin(a) * 4, -math.cos(a) * 4
        ekor = (c - 16 * math.cos(a), c + 16 * math.sin(a))
        self.create_polygon(tip, (c + nx, c + ny), ekor, (c - nx, c - ny), fill=RED, outline="")
        self.create_oval(c - 9, c - 9, c + 9, c + 9, fill="#162438", outline=CYAN, width=2)
        self.create_oval(c - 3, c - 3, c + 3, c + 3, fill=CYAN, outline="")
        self.create_text(c, c - R * .42, text="APEX", font=(FONT, 8, "bold"), fill=CYAN)
        self.create_text(c, c + R * .5, text=str(max(0, int(round(self.v)))), font=(FONT, 26, "bold"), fill=TEXT)
        self.create_text(c, c + R * .5 + 24, text=self.satuan, font=(FONT, 7, "bold"), fill=MUTED)


# ==========================================
# HEADER (judul gradien bergerak + garis cahaya)
# ==========================================
class Header(tk.Canvas):
    def __init__(self, parent, teks, warna, tinggi, sub):
        super().__init__(parent, height=tinggi, bg=BG_APP, highlightthickness=0, bd=0)
        self.teks, self.warna, self.sub, self.t = teks, warna, sub, 0
        self.f = tkfont.Font(family=FONT, size=20, weight="bold")
        self.cw = [self.f.measure(c) for c in teks]
        self.bind("<Configure>", lambda e: self._bg())
        self.after(30, self._frame)

    def _bg(self):
        self.delete("bg")
        w, h = self.winfo_width(), self.winfo_height()
        awal = lerp(self.warna, BG_APP, .45)
        for i in range(50):
            self.create_rectangle(i * w / 50, 0, (i + 1) * w / 50 + 1, h, fill=lerp(awal, BG_APP, i / 50), outline="", tags="bg")
        self.tag_lower("bg")

    def _frame(self):
        try:
            if not self.winfo_exists():
                return
            w, h, t = self.winfo_width(), self.winfo_height(), self.t
            self.delete("dyn")
            if w > 50:
                total = sum(self.cw)
                x0 = (w - total) / 2
                x, tampil = x0, int(t * 1.2)
                for i, (ch, cw) in enumerate(zip(self.teks, self.cw)):
                    if i < tampil:  # efek mengetik di awal
                        col = grad_color(GRAD + (GRAD[0],), ((x + cw / 2 - x0) / total + t * .01) % 1)
                        self.create_text(x, h * .42, text=ch, anchor="w", font=self.f, fill=col, tags="dyn")
                    x += cw
                self.create_text(w / 2, h * .74, text=self.sub, font=(FONT, 9), fill=MUTED, tags="dyn")
                self.create_line(0, h - 1, w, h - 1, fill=BORDER, tags="dyn")
                sx = (t * 7) % (w + 240) - 120
                self.create_line(sx - 100, h - 2, sx, h - 2, fill=self.warna, width=2, tags="dyn")
                self.create_line(sx - 30, h - 2, sx, h - 2, fill=CYAN, width=2, tags="dyn")
            self.t += 1
            self.after(40, self._frame)
        except tk.TclError:
            pass


def buat_header(parent, teks, warna=HEADER_COLOR, tinggi=100, sub="Apex Garage  •  Sistem Manajemen Kendaraan"):
    header = Header(parent, teks, warna, tinggi, sub)
    header.pack(fill="x")
    return header


# ==========================================
# KARTU, FORM & ENTRY
# ==========================================
def buat_kartu(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=16, border_width=1, border_color=BORDER, **kw)


def buat_form(parent):
    form = buat_kartu(parent)
    form.pack(fill="both", expand=True, padx=35, pady=22)
    return form


def efek_fokus(entry):
    entry.bind("<FocusIn>", lambda e: animate(entry, lambda p: entry.configure(border_color=lerp(BORDER, CYAN, p)), 8))
    entry.bind("<FocusOut>", lambda e: animate(entry, lambda p: entry.configure(border_color=lerp(CYAN, BORDER, p)), 8))


def buat_entry(parent, label_text):
    ctk.CTkLabel(parent, text=label_text, text_color=MUTED, font=fnt(11, True)).pack(anchor="w", padx=28, pady=(8, 0))
    entry = ctk.CTkEntry(parent, height=40, corner_radius=10, fg_color=BG_INPUT, border_color=BORDER, text_color=TEXT, font=fnt(13))
    entry.pack(fill="x", padx=28, pady=(5, 6))
    efek_fokus(entry)
    return entry


# ==========================================
# TOMBOL (warna memudar halus saat hover)
# ==========================================
def _hover(tombol, warna, teks=None):
    terang = lerp(warna, "#FFFFFF", .2)

    def masuk(_e):
        dari = tombol.cget("fg_color")
        animate(tombol, lambda p: tombol.configure(fg_color=lerp(dari, terang, p)), 8)
        if teks:
            tombol.configure(text=teks + "   ➜")

    def keluar(_e):
        dari = tombol.cget("fg_color")
        animate(tombol, lambda p: tombol.configure(fg_color=lerp(dari, warna, p)), 8)
        if teks:
            tombol.configure(text=teks)
    tombol.bind("<Enter>", masuk)
    tombol.bind("<Leave>", keluar)


def buat_tombol(parent, teks, command, warna, fg="white", width=14, side=None):
    tombol = ctk.CTkButton(parent, text=teks, command=command, fg_color=warna, hover=False, text_color=fg, corner_radius=10,
                           height=40, width=width * 10, font=fnt(13, True), cursor="hand2")
    _hover(tombol, warna)
    if side:
        tombol.pack(side=side, padx=5)
    else:
        tombol.pack(fill="x", pady=5)
    return tombol


def buat_menu_button(parent, teks, command, warna):
    tombol = ctk.CTkButton(parent, text=teks, command=command, fg_color=warna, hover=False, text_color="white", corner_radius=14,
                           height=58, font=fnt(15, True), cursor="hand2")
    _hover(tombol, warna, teks)  # saat hover muncul panah ➜
    return tombol


# ==========================================
# KARTU STATISTIK & LABEL TOTAL
# ==========================================
def buat_kartu_stat(parent, judul, warna):
    kartu = ctk.CTkFrame(parent, fg_color=BG_INPUT, corner_radius=12, border_width=1, border_color=BORDER)
    nilai = ctk.CTkLabel(kartu, text="0", text_color=warna, font=fnt(26, True))
    nilai.pack(anchor="w", padx=16, pady=(8, 0))
    ctk.CTkLabel(kartu, text=judul, text_color=MUTED, font=fnt(11)).pack(anchor="w", padx=16, pady=(0, 8))
    kartu.bind("<Enter>", lambda e: animate(kartu, lambda p: kartu.configure(border_color=lerp(BORDER, warna, p)), 8))
    kartu.bind("<Leave>", lambda e: animate(kartu, lambda p: kartu.configure(border_color=lerp(warna, BORDER, p)), 8))
    return kartu, nilai


def buat_label_total(parent):
    label = ctk.CTkLabel(parent, text="🚗 Total Kendaraan: 0", text_color=TEXT, font=fnt(13, True))
    label.pack(side="left", padx=16, pady=12)
    return label


# ==========================================
# TREEVIEW (CustomTkinter tidak punya tabel → ttk bertema gelap)
# ==========================================
def _tags(tree, row):
    t = tree.item(row, "tags")
    return (t,) if isinstance(t, str) else tuple(t)


def buat_treeview(parent):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(FONT, 10, "bold"), background="#16223B", foreground=MUTED, relief="flat", borderwidth=0)
    style.map("Treeview.Heading", background=[("active", "#1B2D4A")])
    style.configure("Treeview", font=(FONT, 10), rowheight=32, background=BG_CARD, fieldbackground=BG_CARD, foreground=TEXT, borderwidth=0)
    style.map("Treeview", background=[("selected", BLUE)], foreground=[("selected", "white")])
    style.configure("Vertical.TScrollbar", background="#1B2D4A", troughcolor=BG_CARD, bordercolor=BG_CARD, arrowcolor=MUTED)
    kolom = ("no", "id", "merek", "model", "tahun", "plat", "status")
    tree = ttk.Treeview(parent, columns=kolom, show="headings")
    for k, judul, lebar, rata in (("no", "No", 50, "center"), ("id", "ID Kendaraan", 130, "w"), ("merek", "Merek", 130, "w"),
                                  ("model", "Model", 150, "w"), ("tahun", "Tahun", 80, "center"),
                                  ("plat", "Plat Nomor", 130, "center"), ("status", "Status", 120, "center")):
        tree.heading(k, text=judul)
        tree.column(k, width=lebar, anchor=rata)
    tree.tag_configure("Tersedia", foreground=GREEN)
    tree.tag_configure("Dalam Servis", foreground=YELLOW)
    tree.tag_configure("Nonaktif", foreground=MUTED)
    tree.tag_configure("odd", background="#0F1829")
    tree.tag_configure("hover", background="#1A2B44")
    sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
    sb.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=12)
    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)
    state = {"row": None}

    def gerak(e):
        row = tree.identify_row(e.y) or None
        if row == state["row"]:
            return
        if state["row"] and tree.exists(state["row"]):
            tree.item(state["row"], tags=tuple(t for t in _tags(tree, state["row"]) if t != "hover"))
        state["row"] = row
        if row:
            tree.item(row, tags=_tags(tree, row) + ("hover",))
    tree.bind("<Motion>", gerak)
    tree.bind("<Leave>", lambda e: gerak(type("E", (), {"y": -1})()))
    return tree


def isi_tabel(tree, daftar, animasi=True):
    """Isi tabel dari list Kendaraan; baris muncul bergantian."""
    for job in getattr(tree, "_jobs", []):
        tree.after_cancel(job)
    tree._jobs = []
    tree.delete(*tree.get_children())

    def sisip(n, k):
        try:
            tree.insert("", "end", values=(n, k.id_kendaraan, k.merk, k.model, k.tahun, k.plat_nomor, k.status),
                        tags=(k.status,) + (("odd",) if n % 2 == 0 else ()))
        except tk.TclError:
            pass
    for n, k in enumerate(daftar, start=1):
        if animasi:
            tree._jobs.append(tree.after(min(n, 30) * 22, lambda n=n, k=k: sisip(n, k)))
        else:
            sisip(n, k)
