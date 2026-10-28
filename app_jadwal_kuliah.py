
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- TEMA COQUETTE PINK ---
PINK_BG = "#FFF5F8"
PINK_LIGHT = "#F9E2EA"
PINK_MAIN = "#C56D8B"
PINK_DARK = "#8F3E5A"
PINK_HOVER = "#AD526F"
PINK_BORDER = "#EBC8D5"
WHITE = "#FFFFFF"
TEXT_DARK = "#704656"


def run_jadwal_kuliah():

    # --- KONEKSI DATABASE ---
    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="siakad"
        )

    # --- FUNGSI CRUD ---
    def load_data():
        for row in tree.get_children():
            tree.delete(row)

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT id_jadwal, kode_mk, nip, hari, jam, ruangan
                FROM jadwal_kuliah
            """)

            for index, row in enumerate(cursor.fetchall()):
                tag = "even" if index % 2 == 0 else "odd"
                tree.insert("", "end", values=row, tags=(tag,))

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal mengambil data:\n{e}",
                parent=window_jadwal
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def tambah_data():
        id_jadwal = entry_id.get().strip()
        kode_mk = entry_mk.get().strip()
        nip = entry_nip.get().strip()
        hari = combo_hari.get()
        jam = entry_jam.get().strip()
        ruangan = entry_ruangan.get().strip()

        if not id_jadwal or not kode_mk or not nip:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "ID Jadwal, Kode MK, dan NIP Dosen wajib diisi!",
                parent=window_jadwal
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO jadwal_kuliah
                (id_jadwal, kode_mk, nip, hari, jam, ruangan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (id_jadwal, kode_mk, nip, hari, jam, ruangan)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Jadwal kuliah berhasil ditambahkan!",
                parent=window_jadwal
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menambahkan Jadwal",
                f"Terjadi kesalahan:\n{e}",
                parent=window_jadwal
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def edit_data():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Pilih Data",
                "Pilih jadwal pada tabel terlebih dahulu!",
                parent=window_jadwal
            )
            return

        id_jadwal = entry_id.get().strip()
        kode_mk = entry_mk.get().strip()
        nip = entry_nip.get().strip()
        hari = combo_hari.get()
        jam = entry_jam.get().strip()
        ruangan = entry_ruangan.get().strip()

        if not id_jadwal or not kode_mk or not nip:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "ID Jadwal, Kode MK, dan NIP Dosen wajib diisi!",
                parent=window_jadwal
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE jadwal_kuliah
                SET kode_mk=%s, nip=%s, hari=%s, jam=%s, ruangan=%s
                WHERE id_jadwal=%s
            """

            cursor.execute(
                sql,
                (kode_mk, nip, hari, jam, ruangan, id_jadwal)
            )
            db.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo(
                    "Informasi",
                    "Tidak ada perubahan data atau ID jadwal tidak ditemukan.",
                    parent=window_jadwal
                )
            else:
                messagebox.showinfo(
                    "Berhasil ♡",
                    "Jadwal kuliah berhasil diperbarui!",
                    parent=window_jadwal
                )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Memperbarui Jadwal",
                f"Terjadi kesalahan:\n{e}",
                parent=window_jadwal
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def hapus_data():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Pilih Data",
                "Pilih jadwal pada tabel terlebih dahulu!",
                parent=window_jadwal
            )
            return

        id_jadwal = entry_id.get().strip()

        if not id_jadwal:
            messagebox.showwarning(
                "Pilih Data",
                "ID jadwal tidak ditemukan.",
                parent=window_jadwal
            )
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus jadwal ID {id_jadwal}?",
            parent=window_jadwal
        )

        if not confirm:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM jadwal_kuliah WHERE id_jadwal = %s",
                (id_jadwal,)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Jadwal kuliah berhasil dihapus!",
                parent=window_jadwal
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Jadwal",
                f"Terjadi kesalahan:\n{e}",
                parent=window_jadwal
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def select_item(event=None):
        selected = tree.selection()

        if selected:
            values = tree.item(selected[0], "values")
            clear_fields()

            entry_id.insert(0, values[0])
            entry_mk.insert(0, values[1])
            entry_nip.insert(0, values[2])
            combo_hari.set(values[3])
            entry_jam.insert(0, values[4])
            entry_ruangan.insert(0, values[5])

    def clear_fields():
        entry_id.delete(0, tk.END)
        entry_mk.delete(0, tk.END)
        entry_nip.delete(0, tk.END)
        combo_hari.set("")
        entry_jam.delete(0, tk.END)
        entry_ruangan.delete(0, tk.END)

        for item in tree.selection():
            tree.selection_remove(item)

        entry_id.focus_set()

    # --- GUI WINDOW ---
    window_jadwal = tk.Toplevel()
    window_jadwal.title("♡ Jadwal Kuliah | SIAKAD")
    window_jadwal.geometry("1100x680")
    window_jadwal.minsize(850, 550)
    window_jadwal.configure(bg=PINK_BG)

    # --- STYLE WIDGET ---
    style = ttk.Style(window_jadwal)
    style.theme_use("clam")

    style.configure(
        "Pink.TCombobox",
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT_DARK,
        padding=7
    )

    style.configure(
        "Pink.Treeview",
        background=WHITE,
        foreground=TEXT_DARK,
        fieldbackground=WHITE,
        rowheight=36,
        font=("Segoe UI", 10),
        borderwidth=0
    )

    style.configure(
        "Pink.Treeview.Heading",
        background=PINK_MAIN,
        foreground=WHITE,
        font=("Segoe UI", 10, "bold"),
        padding=(9, 11),
        relief="flat"
    )

    style.map(
        "Pink.Treeview",
        background=[("selected", PINK_LIGHT)],
        foreground=[("selected", TEXT_DARK)]
    )

    style.map(
        "Pink.Treeview.Heading",
        background=[("active", PINK_HOVER)]
    )

    # --- HEADER ---
    header = tk.Frame(window_jadwal, bg=PINK_MAIN, height=95)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="♡  JADWAL KULIAH  ♡",
        font=("Georgia", 22, "bold"),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=28, pady=(17, 2))

    tk.Label(
        header,
        text="Atur jadwal perkuliahan dengan lebih rapi dan terorganisasi.",
        font=("Segoe UI", 10),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=30)

    # --- AREA KONTEN ---
    content = tk.Frame(window_jadwal, bg=PINK_BG)
    content.pack(fill="both", expand=True, padx=24, pady=18)

    # --- FORM DATA JADWAL ---
    frame_form = tk.LabelFrame(
        content,
        text="  ♡ Informasi Jadwal Kuliah  ",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        bd=1,
        relief="solid",
        highlightbackground=PINK_BORDER,
        padx=16,
        pady=14
    )
    frame_form.pack(fill="x", pady=(0, 14))

    def buat_label(teks, row, col):
        tk.Label(
            frame_form,
            text=teks,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        ).grid(
            row=row, column=col,
            sticky="w", padx=(8, 12), pady=9
        )

    def buat_entry(row, col):
        entry = tk.Entry(
            frame_form,
            font=("Segoe UI", 10),
            bg="#FFFAFC",
            fg=TEXT_DARK,
            insertbackground=PINK_DARK,
            relief="flat",
            highlightthickness=1,
            highlightbackground=PINK_BORDER,
            highlightcolor=PINK_MAIN
        )
        entry.grid(
            row=row, column=col,
            sticky="ew", padx=(0, 20), pady=7, ipady=6
        )
        return entry

    buat_label("ID Jadwal", 0, 0)
    entry_id = buat_entry(0, 1)

    buat_label("Kode Mata Kuliah", 0, 2)
    entry_mk = buat_entry(0, 3)

    buat_label("NIP Dosen", 1, 0)
    entry_nip = buat_entry(1, 1)

    buat_label("Hari", 1, 2)
    combo_hari = ttk.Combobox(
        frame_form,
        values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
        state="readonly",
        style="Pink.TCombobox",
        font=("Segoe UI", 10)
    )
    combo_hari.grid(
        row=1, column=3,
        sticky="ew", padx=(0, 20), pady=7
    )

    buat_label("Jam Kuliah", 2, 0)
    entry_jam = buat_entry(2, 1)

    buat_label("Ruangan", 2, 2)
    entry_ruangan = buat_entry(2, 3)

    frame_form.grid_columnconfigure(1, weight=1, uniform="form")
    frame_form.grid_columnconfigure(3, weight=1, uniform="form")

    # --- TOMBOL AKSI ---
    frame_btn = tk.Frame(content, bg=PINK_BG)
    frame_btn.pack(fill="x", pady=(0, 14))

    def buat_tombol(teks, warna, perintah, hover):
        tombol = tk.Button(
            frame_btn,
            text=teks,
            font=("Segoe UI", 10, "bold"),
            bg=warna,
            fg=WHITE,
            activebackground=hover,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=perintah,
            padx=20,
            pady=9
        )
        tombol.pack(side="left", padx=(0, 9))
        tombol.bind(
            "<Enter>",
            lambda event: tombol.config(bg=hover)
        )
        tombol.bind(
            "<Leave>",
            lambda event: tombol.config(bg=warna)
        )
        return tombol

    buat_tombol("+  Tambah", PINK_MAIN, tambah_data, PINK_HOVER)
    buat_tombol("✎  Edit", "#A879A0", edit_data, "#8F6086")
    buat_tombol("⌫  Hapus", PINK_DARK, hapus_data, "#713047")
    buat_tombol("↺  Clear", "#B99AA7", clear_fields, "#9F7F8D")

    # --- TABEL DATA JADWAL ---
    frame_table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=PINK_BORDER,
        highlightthickness=1
    )
    frame_table.pack(fill="both", expand=True)

    tk.Label(
        frame_table,
        text="  ♡ Daftar Jadwal Kuliah",
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        anchor="w"
    ).pack(fill="x", padx=10, pady=(10, 8))

    table_area = tk.Frame(frame_table, bg=WHITE)
    table_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    columns = ("id_jadwal", "kode_mk", "nip", "hari", "jam", "ruangan")

    tree = ttk.Treeview(
        table_area,
        columns=columns,
        show="headings",
        style="Pink.Treeview"
    )

    headers = {
        "id_jadwal": "ID Jadwal",
        "kode_mk": "Kode Mata Kuliah",
        "nip": "NIP Dosen",
        "hari": "Hari",
        "jam": "Jam Kuliah",
        "ruangan": "Ruangan"
    }

    widths = {
        "id_jadwal": 110,
        "kode_mk": 180,
        "nip": 180,
        "hari": 140,
        "jam": 180,
        "ruangan": 150
    }

    for col in columns:
        tree.heading(col, text=headers[col])
        tree.column(
            col,
            width=widths[col],
            minwidth=90,
            anchor="w",
            stretch=True
        )

    scrollbar_y = ttk.Scrollbar(
        table_area,
        orient="vertical",
        command=tree.yview
    )

    scrollbar_x = ttk.Scrollbar(
        table_area,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    table_area.grid_rowconfigure(0, weight=1)
    table_area.grid_columnconfigure(0, weight=1)

    tree.tag_configure("even", background=WHITE)
    tree.tag_configure("odd", background="#FFF4F8")

    tree.bind("<<TreeviewSelect>>", select_item)

    # --- TAMPILKAN DATA AWAL ---
    load_data()
