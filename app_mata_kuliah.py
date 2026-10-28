
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


def run_mata_kuliah():

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
                SELECT kode_mk, nama_mk, sks, semester
                FROM mata_kuliah
            """)

            for index, row in enumerate(cursor.fetchall()):
                tag = "even" if index % 2 == 0 else "odd"
                tree.insert("", "end", values=row, tags=(tag,))

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal mengambil data:\n{e}",
                parent=window_mk
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def tambah_data():
        kode_mk = entry_kode.get().strip()
        nama_mk = entry_nama.get().strip()
        sks = entry_sks.get().strip()
        semester = entry_semester.get().strip()

        if not kode_mk or not nama_mk:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "Kode MK dan Nama Mata Kuliah wajib diisi!",
                parent=window_mk
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO mata_kuliah
                (kode_mk, nama_mk, sks, semester)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (kode_mk, nama_mk, sks, semester)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data mata kuliah berhasil ditambahkan!",
                parent=window_mk
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menambahkan Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mk
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
                "Pilih mata kuliah pada tabel terlebih dahulu!",
                parent=window_mk
            )
            return

        kode_mk = entry_kode.get().strip()
        nama_mk = entry_nama.get().strip()
        sks = entry_sks.get().strip()
        semester = entry_semester.get().strip()

        if not kode_mk or not nama_mk:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "Kode MK dan Nama Mata Kuliah wajib diisi!",
                parent=window_mk
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE mata_kuliah
                SET nama_mk=%s, sks=%s, semester=%s
                WHERE kode_mk=%s
            """

            cursor.execute(
                sql,
                (nama_mk, sks, semester, kode_mk)
            )
            db.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo(
                    "Informasi",
                    "Tidak ada perubahan data atau kode MK tidak ditemukan.",
                    parent=window_mk
                )
            else:
                messagebox.showinfo(
                    "Berhasil ♡",
                    "Data mata kuliah berhasil diperbarui!",
                    parent=window_mk
                )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Memperbarui Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mk
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
                "Pilih mata kuliah pada tabel terlebih dahulu!",
                parent=window_mk
            )
            return

        kode_mk = entry_kode.get().strip()

        if not kode_mk:
            messagebox.showwarning(
                "Pilih Data",
                "Kode mata kuliah tidak ditemukan.",
                parent=window_mk
            )
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus mata kuliah {kode_mk}?",
            parent=window_mk
        )

        if not confirm:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM mata_kuliah WHERE kode_mk = %s",
                (kode_mk,)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data mata kuliah berhasil dihapus!",
                parent=window_mk
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mk
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

            entry_kode.delete(0, tk.END)
            entry_nama.delete(0, tk.END)
            entry_sks.delete(0, tk.END)
            entry_semester.delete(0, tk.END)

            entry_kode.insert(0, values[0])
            entry_nama.insert(0, values[1])
            entry_sks.insert(0, values[2])
            entry_semester.insert(0, values[3])

    def clear_fields():
        entry_kode.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        entry_sks.delete(0, tk.END)
        entry_semester.delete(0, tk.END)

        for item in tree.selection():
            tree.selection_remove(item)

        entry_kode.focus_set()

    # --- JENDELA UTAMA FORM ---
    window_mk = tk.Toplevel()
    window_mk.title("♡ Data Mata Kuliah | SIAKAD")
    window_mk.geometry("1050x650")
    window_mk.minsize(800, 520)
    window_mk.configure(bg=PINK_BG)

    # --- STYLE TABEL ---
    style = ttk.Style(window_mk)
    style.theme_use("clam")

    style.configure(
        "Pink.Treeview",
        background=WHITE,
        foreground=TEXT_DARK,
        fieldbackground=WHITE,
        rowheight=38,
        font=("Segoe UI", 10),
        borderwidth=0
    )

    style.configure(
        "Pink.Treeview.Heading",
        background=PINK_MAIN,
        foreground=WHITE,
        font=("Segoe UI", 10, "bold"),
        padding=(10, 12),
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
    header = tk.Frame(
        window_mk,
        bg=PINK_MAIN,
        height=95
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="♡  DATA MATA KULIAH  ♡",
        font=("Georgia", 22, "bold"),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=28, pady=(17, 2))

    tk.Label(
        header,
        text="Kelola informasi mata kuliah, jumlah SKS, dan semester.",
        font=("Segoe UI", 10),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=30)

    # --- AREA KONTEN ---
    content = tk.Frame(
        window_mk,
        bg=PINK_BG
    )
    content.pack(
        fill="both",
        expand=True,
        padx=24,
        pady=18
    )

    # --- FORM DATA ---
    frame_form = tk.LabelFrame(
        content,
        text="  ♡ Informasi Mata Kuliah  ",
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
            row=row,
            column=col,
            sticky="w",
            padx=(8, 12),
            pady=10
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
            row=row,
            column=col,
            sticky="ew",
            padx=(0, 20),
            pady=8,
            ipady=7
        )
        return entry

    buat_label("Kode Mata Kuliah", 0, 0)
    entry_kode = buat_entry(0, 1)

    buat_label("Nama Mata Kuliah", 0, 2)
    entry_nama = buat_entry(0, 3)

    buat_label("Jumlah SKS", 1, 0)
    entry_sks = buat_entry(1, 1)

    buat_label("Semester", 1, 2)
    entry_semester = buat_entry(1, 3)

    frame_form.grid_columnconfigure(1, weight=1, uniform="form")
    frame_form.grid_columnconfigure(3, weight=1, uniform="form")

    # --- TOMBOL AKSI ---
    frame_btn = tk.Frame(
        content,
        bg=PINK_BG
    )
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

    # --- TABEL DATA ---
    frame_table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=PINK_BORDER,
        highlightthickness=1
    )
    frame_table.pack(fill="both", expand=True)

    tk.Label(
        frame_table,
        text="  ♡ Daftar Mata Kuliah",
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        anchor="w"
    ).pack(fill="x", padx=10, pady=(10, 8))

    table_area = tk.Frame(
        frame_table,
        bg=WHITE
    )
    table_area.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0, 10)
    )

    columns = ("kode_mk", "nama_mk", "sks", "semester")

    tree = ttk.Treeview(
        table_area,
        columns=columns,
        show="headings",
        style="Pink.Treeview"
    )

    headers = {
        "kode_mk": "Kode MK",
        "nama_mk": "Nama Mata Kuliah",
        "sks": "SKS",
        "semester": "Semester"
    }

    widths = {
        "kode_mk": 160,
        "nama_mk": 430,
        "sks": 120,
        "semester": 150
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

    # --- TAMPILKAN DATA ---
    load_data()
