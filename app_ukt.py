
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


def run_pembayaran():

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
                SELECT id_pembayaran, nim, jumlah, tanggal_bayar, status
                FROM pembayaran_ukt
            """)

            for index, row in enumerate(cursor.fetchall()):
                tag = "even" if index % 2 == 0 else "odd"
                tree.insert("", "end", values=row, tags=(tag,))

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Gagal mengambil data:\n{e}",
                parent=window_bayar
            )
        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    def tambah_data():
        id_bayar = entry_id.get().strip()
        nim = entry_nim.get().strip()
        jumlah = entry_jumlah.get().strip()
        tanggal = entry_tanggal.get().strip()
        status = combo_status.get()

        if not id_bayar or not nim or not jumlah:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "ID Pembayaran, NIM, dan Jumlah UKT wajib diisi!",
                parent=window_bayar
            )
            return

        if not jumlah.isdigit():
            messagebox.showwarning(
                "Jumlah Tidak Valid",
                "Jumlah UKT harus berupa angka tanpa pemisah ribuan.",
                parent=window_bayar
            )
            return

        if tanggal:
            try:
                from datetime import date
                date.fromisoformat(tanggal)
            except ValueError:
                messagebox.showwarning(
                    "Tanggal Tidak Valid",
                    "Gunakan format tanggal YYYY-MM-DD, misalnya 2026-10-28.",
                    parent=window_bayar
                )
                return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO pembayaran_ukt
                (id_pembayaran, nim, jumlah, tanggal_bayar, status)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    id_bayar,
                    nim,
                    jumlah,
                    tanggal if tanggal else None,
                    status if status else None
                )
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data pembayaran UKT berhasil ditambahkan!",
                parent=window_bayar
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menambahkan Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_bayar
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
                "Pilih data pembayaran pada tabel terlebih dahulu!",
                parent=window_bayar
            )
            return

        id_bayar = entry_id.get().strip()
        nim = entry_nim.get().strip()
        jumlah = entry_jumlah.get().strip()
        tanggal = entry_tanggal.get().strip()
        status = combo_status.get()

        if not id_bayar or not nim or not jumlah:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "ID Pembayaran, NIM, dan Jumlah UKT wajib diisi!",
                parent=window_bayar
            )
            return

        if not jumlah.isdigit():
            messagebox.showwarning(
                "Jumlah Tidak Valid",
                "Jumlah UKT harus berupa angka tanpa pemisah ribuan.",
                parent=window_bayar
            )
            return

        if tanggal:
            try:
                from datetime import date
                date.fromisoformat(tanggal)
            except ValueError:
                messagebox.showwarning(
                    "Tanggal Tidak Valid",
                    "Gunakan format tanggal YYYY-MM-DD, misalnya 2026-10-28.",
                    parent=window_bayar
                )
                return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE pembayaran_ukt
                SET nim=%s, jumlah=%s, tanggal_bayar=%s, status=%s
                WHERE id_pembayaran=%s
            """

            cursor.execute(
                sql,
                (
                    nim,
                    jumlah,
                    tanggal if tanggal else None,
                    status if status else None,
                    id_bayar
                )
            )
            db.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo(
                    "Informasi",
                    "Tidak ada perubahan data atau ID pembayaran tidak ditemukan.",
                    parent=window_bayar
                )
            else:
                messagebox.showinfo(
                    "Berhasil ♡",
                    "Data pembayaran UKT berhasil diperbarui!",
                    parent=window_bayar
                )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Memperbarui Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_bayar
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
                "Pilih data pembayaran pada tabel terlebih dahulu!",
                parent=window_bayar
            )
            return

        id_bayar = entry_id.get().strip()

        if not id_bayar:
            messagebox.showwarning(
                "Pilih Data",
                "ID pembayaran tidak ditemukan.",
                parent=window_bayar
            )
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus pembayaran ID {id_bayar}?",
            parent=window_bayar
        )

        if not confirm:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM pembayaran_ukt WHERE id_pembayaran = %s",
                (id_bayar,)
            )
            db.commit()

            messagebox.showinfo(
                "Berhasil ♡",
                "Data pembayaran UKT berhasil dihapus!",
                parent=window_bayar
            )

            clear_fields()
            load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Data",
                f"Terjadi kesalahan:\n{e}",
                parent=window_bayar
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

            entry_id.delete(0, tk.END)
            entry_nim.delete(0, tk.END)
            entry_jumlah.delete(0, tk.END)
            entry_tanggal.delete(0, tk.END)

            entry_id.insert(0, values[0])
            entry_nim.insert(0, values[1])
            entry_jumlah.insert(0, values[2])

            if values[3] and str(values[3]) != "None":
                entry_tanggal.insert(0, values[3])

            combo_status.set(
                "" if values[4] is None else values[4]
            )

    def clear_fields():
        entry_id.delete(0, tk.END)
        entry_nim.delete(0, tk.END)
        entry_jumlah.delete(0, tk.END)
        entry_tanggal.delete(0, tk.END)
        combo_status.set("")

        for item in tree.selection():
            tree.selection_remove(item)

        entry_id.focus_set()

    # --- JENDELA FORM ---
    window_bayar = tk.Toplevel()
    window_bayar.title("♡ Pembayaran UKT | SIAKAD")
    window_bayar.geometry("1100x680")
    window_bayar.minsize(850, 550)
    window_bayar.configure(bg=PINK_BG)

    # --- STYLE WIDGET ---
    style = ttk.Style(window_bayar)
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
        window_bayar,
        bg=PINK_MAIN,
        height=95
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="♡  PEMBAYARAN UKT  ♡",
        font=("Georgia", 22, "bold"),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=28, pady=(17, 2))

    tk.Label(
        header,
        text="Kelola informasi pembayaran Uang Kuliah Tunggal mahasiswa.",
        font=("Segoe UI", 10),
        bg=PINK_MAIN,
        fg=WHITE
    ).pack(anchor="w", padx=30)

    # --- AREA KONTEN ---
    content = tk.Frame(
        window_bayar,
        bg=PINK_BG
    )
    content.pack(
        fill="both",
        expand=True,
        padx=24,
        pady=18
    )

    # --- FORM PEMBAYARAN ---
    frame_form = tk.LabelFrame(
        content,
        text="  ♡ Informasi Pembayaran UKT  ",
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
            pady=9
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
            pady=7,
            ipady=6
        )
        return entry

    buat_label("ID Pembayaran", 0, 0)
    entry_id = buat_entry(0, 1)

    buat_label("NIM Mahasiswa", 0, 2)
    entry_nim = buat_entry(0, 3)

    buat_label("Jumlah UKT (Rp)", 1, 0)
    entry_jumlah = buat_entry(1, 1)

    buat_label("Tanggal Bayar (YYYY-MM-DD)", 1, 2)
    entry_tanggal = buat_entry(1, 3)

    buat_label("Status Pembayaran", 2, 0)

    combo_status = ttk.Combobox(
        frame_form,
        values=["Lunas", "Belum Lunas", "Pending"],
        state="readonly",
        style="Pink.TCombobox",
        font=("Segoe UI", 10)
    )
    combo_status.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(0, 20),
        pady=7
    )

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

    # --- TABEL PEMBAYARAN ---
    frame_table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=PINK_BORDER,
        highlightthickness=1
    )
    frame_table.pack(fill="both", expand=True)

    tk.Label(
        frame_table,
        text="  ♡ Daftar Pembayaran UKT",
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

    columns = (
        "id_pembayaran",
        "nim",
        "jumlah",
        "tanggal_bayar",
        "status"
    )

    tree = ttk.Treeview(
        table_area,
        columns=columns,
        show="headings",
        style="Pink.Treeview"
    )

    headers = {
        "id_pembayaran": "ID Pembayaran",
        "nim": "NIM Mahasiswa",
        "jumlah": "Jumlah UKT (Rp)",
        "tanggal_bayar": "Tanggal Bayar",
        "status": "Status"
    }

    widths = {
        "id_pembayaran": 150,
        "nim": 170,
        "jumlah": 180,
        "tanggal_bayar": 180,
        "status": 170
    }

    for col in columns:
        tree.heading(col, text=headers[col])
        tree.column(
            col,
            width=widths[col],
            minwidth=100,
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
