
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
TEXT_MUTED = "#A77C8D"


# --- FUNGSI UTAMA UNTUK MENJALANKAN FORM DOSEN ---
def run_dosen():

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
            cursor.execute(
                "SELECT nip, nama_dosen, jenis_kelamin, email, "
                "no_telepon, pendidikan_terakhir, bidang_keahlian "
                "FROM dosen"
            )

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal mengambil data:\n{e}",
                parent=window_dosen
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def tambah_data():
        nip = entry_nip.get().strip()
        nama = entry_nama.get().strip()
        jk = combo_jk.get()
        email = entry_email.get().strip()
        tlp = entry_tlp.get().strip()
        pendidikan = entry_pendidikan.get().strip()
        bidang = entry_bidang.get().strip()

        if not nip or not nama:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIP dan Nama Dosen wajib diisi!",
                parent=window_dosen
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO dosen
                (nip, nama_dosen, jenis_kelamin, email, no_telepon,
                 pendidikan_terakhir, bidang_keahlian)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            val = (
                nip, nama, jk, email, tlp,
                pendidikan, bidang
            )

            cursor.execute(sql, val)
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data dosen berhasil ditambahkan!",
                parent=window_dosen
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menambahkan Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_dosen
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
                "Pilih data dosen pada tabel terlebih dahulu!",
                parent=window_dosen
            )
            return

        nip = entry_nip.get().strip()
        nama = entry_nama.get().strip()
        jk = combo_jk.get()
        email = entry_email.get().strip()
        tlp = entry_tlp.get().strip()
        pendidikan = entry_pendidikan.get().strip()
        bidang = entry_bidang.get().strip()

        if not nip or not nama:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIP dan Nama Dosen wajib diisi!",
                parent=window_dosen
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE dosen
                SET nama_dosen=%s,
                    jenis_kelamin=%s,
                    email=%s,
                    no_telepon=%s,
                    pendidikan_terakhir=%s,
                    bidang_keahlian=%s
                WHERE nip=%s
            """

            val = (
                nama, jk, email, tlp,
                pendidikan, bidang, nip
            )

            cursor.execute(sql, val)
            db.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo(
                    "Informasi",
                    "Tidak ada perubahan data atau NIP tidak ditemukan.",
                    parent=window_dosen
                )
            else:
                messagebox.showinfo(
                    "Berhasil ♡",
                    "Data dosen berhasil diperbarui!",
                    parent=window_dosen
                )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Memperbarui Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_dosen
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
                "Pilih data dosen pada tabel terlebih dahulu!",
                parent=window_dosen
            )
            return

        nip = entry_nip.get().strip()

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus dosen dengan NIP {nip}?",
            parent=window_dosen
        )

        if not confirm:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM dosen WHERE nip = %s",
                (nip,)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data dosen berhasil dihapus!",
                parent=window_dosen
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_dosen
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

            entry_nip.insert(0, values[0])
            entry_nama.insert(0, values[1])
            combo_jk.set(values[2])
            entry_email.insert(0, values[3])
            entry_tlp.insert(0, values[4])
            entry_pendidikan.insert(0, values[5])
            entry_bidang.insert(0, values[6])

    def clear_fields():
        entry_nip.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        combo_jk.set("")
        entry_email.delete(0, tk.END)
        entry_tlp.delete(0, tk.END)
        entry_pendidikan.delete(0, tk.END)
        entry_bidang.delete(0, tk.END)

        for item in tree.selection():
            tree.selection_remove(item)

        entry_nip.focus_set()

    # --- GUI WINDOW ---
    window_dosen = tk.Toplevel()
    window_dosen.title("♡ Data Dosen | SIAKAD")
    window_dosen.geometry("1180x720")
    window_dosen.minsize(900, 600)
    window_dosen.configure(bg=PINK_BG)

    # --- STYLE WIDGET ---
    style = ttk.Style(window_dosen)
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
        font=("Segoe UI", 10, "bold"),
        padding=(8, 11),
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
    header = tk.Frame(window_dosen, bg=PINK_MAIN, height=95)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="♡  DATA DOSEN  ♡",
        font=("Georgia", 22, "bold"),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=28, pady=(17, 2))

    tk.Label(
        header,
        text="Kelola informasi dosen dengan rapi dan mudah.",
        font=("Segoe UI", 10),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=30)

    # --- AREA KONTEN ---
    content = tk.Frame(window_dosen, bg=PINK_BG)
    content.pack(fill="both", expand=True, padx=24, pady=18)

    # --- FORM DATA DOSEN ---
    frame_form = tk.LabelFrame(
        content,
        text="  ♡ Informasi Dosen  ",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        bd=1,
        relief="solid",
        highlightbackground=PINK_BORDER,
        padx=16,
        pady=12
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

    buat_label("NIP", 0, 0)
    entry_nip = buat_entry(0, 1)

    buat_label("Nama Dosen", 0, 2)
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
        sticky="ew", padx=(0, 20), pady=7
    )

    buat_label("Email", 1, 2)
    entry_email = buat_entry(1, 3)

    buat_label("No. Telepon", 2, 0)
    entry_tlp = buat_entry(2, 1)

    buat_label("Pendidikan Terakhir", 2, 2)
    entry_pendidikan = buat_entry(2, 3)

    buat_label("Bidang Keahlian", 3, 0)
    entry_bidang = buat_entry(3, 1)

    frame_form.grid_columnconfigure(1, weight=1, uniform="form")
    frame_form.grid_columnconfigure(3, weight=1, uniform="form")

    # --- FRAME TOMBOL ---
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

    # --- FRAME TABEL ---
    frame_table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=PINK_BORDER,
        highlightthickness=1
    )
    frame_table.pack(fill="both", expand=True)

    tk.Label(
        frame_table,
        text="  ♡ Daftar Dosen",
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=PINK_DARK,
        anchor="w"
    ).pack(fill="x", padx=10, pady=(10, 8))

    table_area = tk.Frame(frame_table, bg=WHITE)
    table_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    columns = (
        "nip", "nama_dosen", "jenis_kelamin", "email",
        "no_telepon", "pendidikan_terakhir", "bidang_keahlian"
    )

    tree = ttk.Treeview(
        table_area,
        columns=columns,
        show="headings",
        style="Pink.Treeview"
    )

    headings = {
        "nip": "NIP",
        "nama_dosen": "Nama Dosen",
        "jenis_kelamin": "Jenis Kelamin",
        "email": "Email",
        "no_telepon": "No. Telepon",
        "pendidikan_terakhir": "Pendidikan",
        "bidang_keahlian": "Bidang Keahlian"
    }

    widths = {
        "nip": 90,
        "nama_dosen": 190,
        "jenis_kelamin": 120,
        "email": 190,
        "no_telepon": 125,
        "pendidikan_terakhir": 115,
        "bidang_keahlian": 190
    }

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(
            col,
            width=widths[col],
            minwidth=80,
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
