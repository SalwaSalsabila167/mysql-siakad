
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


# --- FUNGSI UTAMA UNTUK MENJALANKAN FORM MAHASISWA ---
def run_mahasiswa():

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
                SELECT nim, nama_lengkap, jenis_kelamin, tanggal_lahir,
                       tempat_lahir, alamat, no_telepon, email,
                       jurusan, angkatan, status
                FROM mahasiswa
            """)

            for index, row in enumerate(cursor.fetchall()):
                tag = "even" if index % 2 == 0 else "odd"
                tree.insert("", "end", values=row, tags=(tag,))

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal mengambil data:\n{e}",
                parent=window_mhs
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def tambah_data():
        nim = entry_nim.get().strip()
        nama = entry_nama.get().strip()
        jk = combo_jk.get()
        tgl_lahir = entry_tgl.get().strip()
        tmpt_lahir = entry_tmpt.get().strip()
        alamat = entry_alamat.get().strip()
        tlp = entry_tlp.get().strip()
        email = entry_email.get().strip()
        jurusan = entry_jurusan.get().strip()
        angkatan = entry_angkatan.get().strip()
        status = combo_status.get()

        if not nim or not nama:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIM dan Nama Lengkap wajib diisi!",
                parent=window_mhs
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO mahasiswa
                (nim, nama_lengkap, jenis_kelamin, tanggal_lahir,
                 tempat_lahir, alamat, no_telepon, email, jurusan,
                 angkatan, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            val = (
                nim, nama, jk, tgl_lahir, tmpt_lahir, alamat,
                tlp, email, jurusan, angkatan, status
            )

            cursor.execute(sql, val)
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data mahasiswa berhasil ditambahkan!",
                parent=window_mhs
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menambahkan Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mhs
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
                "Pilih data mahasiswa pada tabel terlebih dahulu!",
                parent=window_mhs
            )
            return

        nim = entry_nim.get().strip()
        nama = entry_nama.get().strip()
        jk = combo_jk.get()
        tgl_lahir = entry_tgl.get().strip()
        tmpt_lahir = entry_tmpt.get().strip()
        alamat = entry_alamat.get().strip()
        tlp = entry_tlp.get().strip()
        email = entry_email.get().strip()
        jurusan = entry_jurusan.get().strip()
        angkatan = entry_angkatan.get().strip()
        status = combo_status.get()

        if not nim or not nama:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIM dan Nama Lengkap wajib diisi!",
                parent=window_mhs
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE mahasiswa
                SET nama_lengkap=%s, jenis_kelamin=%s,
                    tanggal_lahir=%s, tempat_lahir=%s,
                    alamat=%s, no_telepon=%s, email=%s,
                    jurusan=%s, angkatan=%s, status=%s
                WHERE nim=%s
            """

            val = (
                nama, jk, tgl_lahir, tmpt_lahir, alamat,
                tlp, email, jurusan, angkatan, status, nim
            )

            cursor.execute(sql, val)
            db.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo(
                    "Informasi",
                    "Tidak ada perubahan data atau NIM tidak ditemukan.",
                    parent=window_mhs
                )
            else:
                messagebox.showinfo(
                    "Berhasil ♡",
                    "Data mahasiswa berhasil diperbarui!",
                    parent=window_mhs
                )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Memperbarui Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mhs
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
                "Pilih data mahasiswa pada tabel terlebih dahulu!",
                parent=window_mhs
            )
            return

        nim = entry_nim.get().strip()

        if not nim:
            messagebox.showwarning(
                "Pilih Data",
                "NIM mahasiswa tidak ditemukan.",
                parent=window_mhs
            )
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus mahasiswa dengan NIM {nim}?",
            parent=window_mhs
        )

        if not confirm:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM mahasiswa WHERE nim = %s",
                (nim,)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data mahasiswa berhasil dihapus!",
                parent=window_mhs
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_mhs
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

            entry_nim.insert(0, values[0])
            entry_nama.insert(0, values[1])
            combo_jk.set(values[2])
            entry_tgl.insert(0, values[3])
            entry_tmpt.insert(0, values[4])
            entry_alamat.insert(0, values[5])
            entry_tlp.insert(0, values[6])
            entry_email.insert(0, values[7])
            entry_jurusan.insert(0, values[8])
            entry_angkatan.insert(0, values[9])
            combo_status.set(values[10])

    def clear_fields():
        entry_nim.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        combo_jk.set("")
        entry_tgl.delete(0, tk.END)
        entry_tmpt.delete(0, tk.END)
        entry_alamat.delete(0, tk.END)
        entry_tlp.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_jurusan.delete(0, tk.END)
        entry_angkatan.delete(0, tk.END)
        combo_status.set("")

        for item in tree.selection():
            tree.selection_remove(item)

        entry_nim.focus_set()

    # --- GUI WINDOW ---
    window_mhs = tk.Toplevel()
    window_mhs.title("♡ Data Mahasiswa | SIAKAD")
    window_mhs.geometry("1250x780")
    window_mhs.minsize(950, 650)
    window_mhs.configure(bg=PINK_BG)

    # --- STYLE WIDGET ---
    style = ttk.Style(window_mhs)
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
        rowheight=34,
        font=("Segoe UI", 10),
        borderwidth=0
    )

    style.configure(
        "Pink.Treeview.Heading",
        background=PINK_MAIN,
        foreground=WHITE,
        font=("Segoe UI", 9, "bold"),
        padding=(7, 10),
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
    header = tk.Frame(window_mhs, bg=PINK_MAIN, height=95)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="♡  DATA MAHASISWA  ♡",
        font=("Georgia", 22, "bold"),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=28, pady=(17, 2))

    tk.Label(
        header,
        text="Kelola informasi mahasiswa dengan rapi dan mudah.",
        font=("Segoe UI", 10),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=30)

    # --- AREA KONTEN ---
    content = tk.Frame(window_mhs, bg=PINK_BG)
    content.pack(fill="both", expand=True, padx=22, pady=16)

    # --- FORM DATA MAHASISWA ---
    frame_form = tk.LabelFrame(
        content,
        text="  ♡ Informasi Mahasiswa  ",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        bd=1,
        relief="solid",
        highlightbackground=PINK_BORDER,
        padx=14,
        pady=10
    )
    frame_form.pack(fill="x", pady=(0, 12))

    def buat_label(teks, row, col):
        tk.Label(
            frame_form,
            text=teks,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=TEXT_DARK
        ).grid(
            row=row, column=col,
            sticky="w", padx=(7, 10), pady=6
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
            sticky="ew", padx=(0, 16), pady=5, ipady=5
        )
        return entry

    # Susunan input dua pasang kolom
    buat_label("NIM", 0, 0)
    entry_nim = buat_entry(0, 1)

    buat_label("Nama Lengkap", 0, 2)
    entry_nama = buat_entry(0, 3)

    buat_label("Jenis Kelamin", 1, 0)
    combo_jk = ttk.Combobox(
        frame_form,
        values=["Laki-laki", "Perempuan"],
        state="readonly",
        style="Pink.TCombobox",
        font=("Segoe UI", 10)
    )
    combo_jk.grid(
        row=1, column=1,
        sticky="ew", padx=(0, 16), pady=5
    )

    buat_label("Tanggal Lahir", 1, 2)
    entry_tgl = buat_entry(1, 3)

    buat_label("Tempat Lahir", 2, 0)
    entry_tmpt = buat_entry(2, 1)

    buat_label("Alamat", 2, 2)
    entry_alamat = buat_entry(2, 3)

    buat_label("No. Telepon", 3, 0)
    entry_tlp = buat_entry(3, 1)

    buat_label("Email", 3, 2)
    entry_email = buat_entry(3, 3)

    buat_label("Jurusan", 4, 0)
    entry_jurusan = buat_entry(4, 1)

    buat_label("Angkatan", 4, 2)
    entry_angkatan = buat_entry(4, 3)

    buat_label("Status", 5, 0)
    combo_status = ttk.Combobox(
        frame_form,
        values=["Aktif", "Cuti", "Lulus", "Keluar"],
        state="readonly",
        style="Pink.TCombobox",
        font=("Segoe UI", 10)
    )
    combo_status.grid(
        row=5, column=1,
        sticky="ew", padx=(0, 16), pady=5
    )

    frame_form.grid_columnconfigure(1, weight=1, uniform="form")
    frame_form.grid_columnconfigure(3, weight=1, uniform="form")

    # --- TOMBOL AKSI ---
    frame_btn = tk.Frame(content, bg=PINK_BG)
    frame_btn.pack(fill="x", pady=(0, 12))

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
            padx=18,
            pady=8
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

    # --- TABEL DATA MAHASISWA ---
    frame_table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=PINK_BORDER,
        highlightthickness=1
    )
    frame_table.pack(fill="both", expand=True)

    tk.Label(
        frame_table,
        text="  ♡ Daftar Mahasiswa",
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        anchor="w"
    ).pack(fill="x", padx=10, pady=(9, 7))

    table_area = tk.Frame(frame_table, bg=WHITE)
    table_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    columns = (
        "nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir",
        "tempat_lahir", "alamat", "no_telepon", "email",
        "jurusan", "angkatan", "status"
    )

    tree = ttk.Treeview(
        table_area,
        columns=columns,
        show="headings",
        style="Pink.Treeview"
    )

    headers = {
        "nim": "NIM",
        "nama_lengkap": "Nama Lengkap",
        "jenis_kelamin": "Jenis Kelamin",
        "tanggal_lahir": "Tanggal Lahir",
        "tempat_lahir": "Tempat Lahir",
        "alamat": "Alamat",
        "no_telepon": "No. Telepon",
        "email": "Email",
        "jurusan": "Jurusan",
        "angkatan": "Angkatan",
        "status": "Status"
    }

    widths = {
        "nim": 90,
        "nama_lengkap": 165,
        "jenis_kelamin": 115,
        "tanggal_lahir": 110,
        "tempat_lahir": 120,
        "alamat": 190,
        "no_telepon": 125,
        "email": 180,
        "jurusan": 130,
        "angkatan": 85,
        "status": 90
    }

    for col in columns:
        tree.heading(col, text=headers[col])
        tree.column(
            col,
            width=widths[col],
            minwidth=75,
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
