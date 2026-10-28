
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# =========================================================
# KONFIGURASI DATABASE DAN TEMA
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "siakad"
}

BG = "#FFF5F8"
PINK_LIGHT = "#F9E2EA"
PINK_PALE = "#FFF0F4"
PINK_MAIN = "#C76D8A"
PINK_HOVER = "#AD526F"
PINK_DARK = "#8F3E5A"
BORDER = "#EBC8D5"
WHITE = "#FFFFFF"
TEXT = "#704656"
MUTED = "#A17D8B"


# Nama tabel, kolom, dan kunci utama.
# Sesuaikan jika nama kolom pada database kamu berbeda.
FORM_CONFIG = {
    "Data Dosen": {
        "table": "dosen",
        "pk": "nip",
        "fields": [
            "nip", "nama_dosen", "jenis_kelamin", "email",
            "no_telepon", "pendidikan_terakhir", "bidang_keahlian"
        ],
        "labels": {
            "nip": "NIP",
            "nama_dosen": "Nama Dosen",
            "jenis_kelamin": "Jenis Kelamin",
            "email": "Email",
            "no_telepon": "Nomor Telepon",
            "pendidikan_terakhir": "Pendidikan Terakhir",
            "bidang_keahlian": "Bidang Keahlian"
        }
    },
    "Data Mahasiswa": {
        "table": "mahasiswa",
        "pk": "nim",
        "fields": [
            "nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir",
            "tempat_lahir", "alamat", "no_telepon", "email",
            "jurusan", "angkatan", "status"
        ],
        "labels": {
            "nim": "NIM",
            "nama_lengkap": "Nama Lengkap",
            "jenis_kelamin": "Jenis Kelamin",
            "tanggal_lahir": "Tanggal Lahir (YYYY-MM-DD)",
            "tempat_lahir": "Tempat Lahir",
            "alamat": "Alamat",
            "no_telepon": "Nomor Telepon",
            "email": "Email",
            "jurusan": "Jurusan",
            "angkatan": "Angkatan",
            "status": "Status"
        }
    },
    "Mata Kuliah": {
        "table": "mata_kuliah",
        "pk": "kode_mk",
        "fields": ["kode_mk", "nama_mk", "sks", "semester"],
        "labels": {
            "kode_mk": "Kode Mata Kuliah",
            "nama_mk": "Nama Mata Kuliah",
            "sks": "Jumlah SKS",
            "semester": "Semester"
        }
    },
    "Jadwal Kuliah": {
        "table": "jadwal_kuliah",
        "pk": "id_jadwal",
        "fields": [
            "id_jadwal", "kode_mk", "hari", "jam_mulai", "jam_selesai", "ruangan"
        ],
        "labels": {
            "id_jadwal": "ID Jadwal",
            "kode_mk": "Kode Mata Kuliah",
            "hari": "Hari",
            "jam": "Jam Mulai",
            "jam": "Jam Selesai",
            "ruangan": "Ruangan"
        }
    },
    
"Data KRS": {
    "table": "krs",
    "pk": "id_krs",
    "fields": [
        "id_krs",
        "nim",
        "kode_mk",
        "semester_ambil",
        "tahun_ajaran",
        "nilai_huruf",
        "nilai_angka"
    ],
    "labels": {
        "id_krs": "ID KRS",
        "nim": "NIM",
        "kode_mk": "Kode Mata Kuliah",
        "semester_ambil": "Semester Diambil",
        "tahunajaran": "Tahun Ajaran",
        "nilai_huruf": "Nilai Huruf",
        "nilai_angka": "Nilai Angka"
    }
},

"Pembayaran UKT": {
    "table": "pembayaran_ukt",
    "pk": "id_pembayaran",
    "fields": [
        "id_pembayaran",
        "nim",
        "semester",
        "tahun_ajaran",
        "jumlah_bayar",
        "tanggal_bayar",
        "metode_pembayaran",
        "status"
    ],
    "labels": {
        "id_pembayaran": "ID Pembayaran",
        "nim": "NIM",
        "semester": "Semester",
        "tahun_ajaran": "Tahun Ajaran",
        "jumlah_bayar": "Jumlah Bayar (Rp)",
        "tanggal_bayar": "Tanggal Bayar (YYYY-MM-DD)",
        "metode_pembayaran": "Metode Pembayaran",
        "status": "Status Pembayaran"
    }
}
}


# =========================================================
# APLIKASI UTAMA
# =========================================================

class SiakadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD - Coquette Pink Edition")
        self.root.configure(bg=BG)

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1200x750")

        self.root.minsize(900, 600)
        self.current_user = None
        self.content = None

        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Pink.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=29,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Pink.Treeview.Heading",
            background=PINK_LIGHT,
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
            padding=8
        )
        style.map(
            "Pink.Treeview",
            background=[("selected", PINK_MAIN)],
            foreground=[("selected", WHITE)]
        )

    def connect_db(self):
        return mysql.connector.connect(**DB_CONFIG)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # =====================================================
    # LOGIN
    # =====================================================

    def show_login(self):
        self.clear_root()
        self.root.unbind("<Return>")

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(
            outer, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=45, pady=35
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="୨୧  ♡  ୨୧",
            font=("Segoe UI", 20),
            bg=WHITE, fg=PINK_MAIN
        ).pack(pady=(0, 8))

        tk.Label(
            card, text="SIAKAD",
            font=("Georgia", 30, "bold"),
            bg=WHITE, fg=PINK_MAIN
        ).pack()

        tk.Label(
            card, text="SISTEM INFORMASI AKADEMIK",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE, fg=MUTED
        ).pack(pady=(3, 5))

        tk.Label(
            card, text="♡  Welcome back!  ♡",
            font=("Georgia", 12, "italic"),
            bg=WHITE, fg=TEXT
        ).pack(pady=(0, 22))

        tk.Label(
            card, text="Username (NIP)",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE, fg=TEXT, anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.entry_nip = tk.Entry(
            card, font=("Segoe UI", 11),
            width=32, relief="flat",
            bg=PINK_PALE, fg=TEXT,
            insertbackground=PINK_MAIN
        )
        self.entry_nip.pack(fill="x", ipady=10, pady=(0, 14))

        tk.Label(
            card, text="Password (Email)",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE, fg=TEXT, anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.entry_email = tk.Entry(
            card, font=("Segoe UI", 11),
            width=32, show="*",
            relief="flat", bg=PINK_PALE,
            fg=TEXT, insertbackground=PINK_MAIN
        )
        self.entry_email.pack(fill="x", ipady=10)

        btn = tk.Button(
            card, text="♡   LOGIN   ♡",
            font=("Segoe UI", 11, "bold"),
            bg=PINK_MAIN, fg=WHITE,
            activebackground=PINK_HOVER,
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            command=self.proses_login
        )
        btn.pack(fill="x", ipady=9, pady=(20, 12))
        btn.bind("<Enter>", lambda e: btn.config(bg=PINK_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=PINK_MAIN))

        tk.Label(
            card, text="Made with ♡ and a little pink magic",
            font=("Segoe UI", 9, "italic"),
            bg=WHITE, fg=MUTED
        ).pack(pady=(5, 0))

        self.entry_nip.focus_set()
        self.root.bind("<Return>", lambda event: self.proses_login())

    def proses_login(self):
        nip = self.entry_nip.get().strip()
        email = self.entry_email.get().strip()

        if not nip or not email:
            messagebox.showwarning(
                "Peringatan",
                "Username (NIP) dan Password (Email) wajib diisi."
            )
            return

        conn = None
        cursor = None

        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT nip, nama_dosen, email
                FROM dosen
                WHERE nip = %s AND email = %s
                """,
                (nip, email)
            )
            user = cursor.fetchone()

            if user:
                self.current_user = user
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Gagal",
                    "NIP atau email tidak sesuai."
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Tidak dapat mengakses database:\n{err}"
            )
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # =====================================================
    # DASHBOARD DAN NAVIGASI
    # =====================================================

    def show_dashboard(self):
        self.clear_root()
        self.root.unbind("<Return>")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        sidebar = tk.Frame(self.root, bg=PINK_MAIN, width=245)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar, text="୨୧  ♡  ୨୧",
            font=("Segoe UI", 20),
            bg=PINK_MAIN, fg=WHITE
        ).pack(pady=(28, 5))

        tk.Label(
            sidebar, text="SIAKAD",
            font=("Georgia", 25, "bold"),
            bg=PINK_MAIN, fg=WHITE
        ).pack()

        tk.Label(
            sidebar, text="ACADEMIC PORTAL",
            font=("Segoe UI", 9, "bold"),
            bg=PINK_MAIN, fg="#FFEAF0"
        ).pack(pady=(3, 24))

        tk.Frame(sidebar, bg="#E9AFC2", height=1).pack(
            fill="x", padx=22, pady=(0, 18)
        )

        tk.Label(
            sidebar,
            text=f"♡  {self.current_user['nama_dosen']}",
            font=("Segoe UI", 10, "bold"),
            bg=PINK_MAIN, fg=WHITE,
            wraplength=200, justify="left"
        ).pack(fill="x", padx=20, pady=(0, 18))

        self.nav_button(sidebar, "♡  Dashboard", self.show_home)

        for menu in FORM_CONFIG:
            self.nav_button(
                sidebar, "♡  " + menu,
                lambda m=menu: self.show_crud(m)
            )

        tk.Frame(sidebar, bg="#E9AFC2", height=1).pack(
            fill="x", padx=22, pady=(20, 12)
        )

        tk.Button(
            sidebar, text="♡  Keluar",
            font=("Segoe UI", 10, "bold"),
            bg=PINK_DARK, fg=WHITE,
            activebackground="#713047",
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            command=self.konfirmasi_keluar
        ).pack(fill="x", padx=14, pady=5, ipady=9)

        self.content = tk.Frame(self.root, bg=BG)
        self.content.grid(
            row=0, column=1, sticky="nsew",
            padx=28, pady=25
        )
        self.show_home()

    def nav_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text,
            font=("Segoe UI", 10, "bold"),
            bg=PINK_MAIN, fg=WHITE,
            activebackground=PINK_HOVER,
            activeforeground=WHITE,
            relief="flat", bd=0,
            anchor="w", padx=20, pady=10,
            cursor="hand2", command=command
        )
        btn.pack(fill="x", padx=10, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg=PINK_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=PINK_MAIN))

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Welcome to Your Dashboard  ♡",
            font=("Georgia", 24, "bold"),
            bg=BG, fg=TEXT, anchor="w"
        ).pack(fill="x", pady=(0, 8))

        tk.Label(
            self.content,
            text=f"Halo, {self.current_user['nama_dosen']}! "
                 "Selamat datang di SIAKAD.",
            font=("Segoe UI", 11),
            bg=BG, fg=MUTED, anchor="w"
        ).pack(fill="x", pady=(0, 22))

        banner = tk.Frame(self.content, bg=PINK_LIGHT, padx=24, pady=22)
        banner.pack(fill="x", pady=(0, 22))

        tk.Label(
            banner,
            text="୨୧  A Little Pink, A Lot of Productivity  ୨୧",
            font=("Georgia", 17, "bold"),
            bg=PINK_LIGHT, fg=PINK_MAIN
        ).pack(anchor="w")

        tk.Label(
            banner,
            text="Pilih menu untuk mengelola informasi akademik.",
            font=("Segoe UI", 10),
            bg=PINK_LIGHT, fg=TEXT
        ).pack(anchor="w", pady=(8, 0))

        tk.Label(
            self.content, text="♡  Academic Management",
            font=("Georgia", 16, "bold"),
            bg=BG, fg=TEXT
        ).pack(anchor="w", pady=(0, 12))

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="both", expand=True)

        for col in range(3):
            cards.grid_columnconfigure(col, weight=1, uniform="cards")
        for row in range(2):
            cards.grid_rowconfigure(row, weight=1, uniform="cards")

        descriptions = {
            "Data Dosen": "Kelola informasi dosen.",
            "Data Mahasiswa": "Kelola data mahasiswa.",
            "Mata Kuliah": "Kelola informasi mata kuliah.",
            "Jadwal Kuliah": "Kelola jadwal perkuliahan.",
            "Data KRS": "Kelola kartu rencana studi.",
            "Pembayaran UKT": "Kelola data pembayaran UKT."
        }
        icons = ["♡", "୨୧", "✿", "♡", "✧", "₊˚"]

        for index, menu in enumerate(FORM_CONFIG):
            row, col = divmod(index, 3)
            card = tk.Frame(
                cards, bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1, padx=15, pady=13
            )
            card.grid(
                row=row, column=col, sticky="nsew",
                padx=7, pady=7
            )

            tk.Label(
                card, text=icons[index],
                font=("Segoe UI", 23),
                bg=WHITE, fg=PINK_MAIN
            ).pack(anchor="w")

            tk.Label(
                card, text=menu,
                font=("Segoe UI", 11, "bold"),
                bg=WHITE, fg=TEXT, anchor="w"
            ).pack(anchor="w", pady=(5, 4))

            tk.Label(
                card, text=descriptions[menu],
                font=("Segoe UI", 9),
                bg=WHITE, fg=MUTED, anchor="w",
                wraplength=200, justify="left"
            ).pack(anchor="w", pady=(0, 10))

            tk.Button(
                card, text="Buka Menu  ♡",
                font=("Segoe UI", 9, "bold"),
                bg=PINK_LIGHT, fg=PINK_DARK,
                activebackground=PINK_MAIN,
                activeforeground=WHITE,
                relief="flat", cursor="hand2",
                command=lambda m=menu: self.show_crud(m)
            ).pack(anchor="w", ipadx=8, ipady=5)

        tk.Label(
            self.content,
            text="Made with ♡  |  SIAKAD Academic System",
            font=("Segoe UI", 9, "italic"),
            bg=BG, fg=MUTED
        ).pack(pady=(12, 0))

    def konfirmasi_keluar(self):
        if messagebox.askyesno(
            "Keluar",
            "Kembali ke halaman login?"
        ):
            self.current_user = None
            self.show_login()


    # =====================================================
    # FORM CRUD DINAMIS
    # =====================================================

    def show_crud(self, menu):
        self.clear_content()
        config = FORM_CONFIG[menu]

        tk.Label(
            self.content, text=menu + "  ♡",
            font=("Georgia", 22, "bold"),
            bg=BG, fg=TEXT, anchor="w"
        ).pack(fill="x", pady=(0, 4))

        tk.Label(
            self.content,
            text="Kelola data menggunakan formulir di bawah ini.",
            font=("Segoe UI", 10),
            bg=BG, fg=MUTED, anchor="w"
        ).pack(fill="x", pady=(0, 15))

        form_card = tk.Frame(
            self.content, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1, padx=15, pady=12
        )
        form_card.pack(fill="x", pady=(0, 14))

        fields = config["fields"]
        labels = config["labels"]
        entries = {}

        # Atur jumlah kolom berdasarkan banyaknya field.
        form_columns = 3 if len(fields) > 6 else 2
        for col in range(form_columns * 2):
            form_card.grid_columnconfigure(col, weight=1)

        for i, field in enumerate(fields):
            row = (i // form_columns) * 2
            col = (i % form_columns) * 2

            tk.Label(
                form_card, text=labels.get(field, field),
                font=("Segoe UI", 9, "bold"),
                bg=WHITE, fg=TEXT, anchor="w"
            ).grid(
                row=row, column=col, sticky="w",
                padx=5, pady=(3, 3)
            )

            if field == "hari":
                widget = ttk.Combobox(
                    form_card,
                    values=[
                        "Senin", "Selasa", "Rabu",
                        "Kamis", "Jumat", "Sabtu"
                    ],
                    state="readonly",
                    font=("Segoe UI", 9)
                )
            elif field == "status" and menu == "Pembayaran UKT":
                widget = ttk.Combobox(
                    form_card,
                    values=["Lunas", "Belum Lunas", "Pending"],
                    state="readonly",
                    font=("Segoe UI", 9)
                )
            else:
                widget = tk.Entry(
                    form_card, font=("Segoe UI", 9),
                    relief="solid", bd=1,
                    bg=PINK_PALE, fg=TEXT,
                    insertbackground=PINK_MAIN
                )

            widget.grid(
                row=row + 1, column=col,
                columnspan=2, sticky="ew",
                padx=5, pady=(0, 8), ipady=5
            )
            entries[field] = widget

        selected = {"pk": None}

        # Tombol aksi
        action_frame = tk.Frame(form_card, bg=WHITE)
        action_frame.grid(
            row=((len(fields) + form_columns - 1) // form_columns) * 2,
            column=0, columnspan=form_columns * 2,
            sticky="w", pady=(5, 0)
        )

        table_frame = tk.Frame(self.content, bg=BG)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            table_frame,
            columns=fields,
            show="headings",
            style="Pink.Treeview"
        )

        for field in fields:
            tree.heading(field, text=labels.get(field, field))
            tree.column(field, width=120, minwidth=80, anchor="w")

        yscroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=tree.yview
        )
        xscroll = ttk.Scrollbar(
            table_frame, orient="horizontal", command=tree.xview
        )
        tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        def get_connection():
            return self.connect_db()

        def load_data():
            for item in tree.get_children():
                tree.delete(item)

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                column_sql = ", ".join(f"`{f}`" for f in fields)
                cursor.execute(
                    f"SELECT {column_sql} FROM `{config['table']}`"
                )

                for row in cursor.fetchall():
                    tree.insert("", "end", values=[
                        "" if value is None else str(value)
                        for value in row
                    ])

            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Database Error",
                    f"Gagal memuat data {menu}:\n{err}"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        def clear_form():
            for widget in entries.values():
                if isinstance(widget, ttk.Combobox):
                    widget.set("")
                else:
                    widget.delete(0, tk.END)
            selected["pk"] = None
            tree.selection_remove(tree.selection())

        def select_row(event=None):
            chosen = tree.selection()
            if not chosen:
                return

            values = tree.item(chosen[0], "values")
            for field, value in zip(fields, values):
                widget = entries[field]
                if isinstance(widget, ttk.Combobox):
                    widget.set(value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)

            pk_index = fields.index(config["pk"])
            selected["pk"] = values[pk_index]

        def save_data():
            values = {
                field: entries[field].get().strip()
                for field in fields
            }

            # ID otomatis boleh dikosongkan saat menambah data.
            # Kolom harus benar-benar AUTO_INCREMENT di database.
            auto_pk_fields = {"id_jadwal", "id_krs", "id_pembayaran"}
            pk = config["pk"]

            missing = [
                labels.get(field, field)
                for field, value in values.items()
                if not value and not (
                    field == pk
                    and field in auto_pk_fields
                    and selected["pk"] is None
                )
            ]
            if missing:
                messagebox.showwarning(
                    "Data Belum Lengkap",
                    "Lengkapi kolom berikut:\n- " + "\n- ".join(missing)
                )
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()

                if selected["pk"] is None:
                    insert_fields = [
                        field for field in fields
                        if not (
                            field == pk
                            and field in auto_pk_fields
                            and not values[field]
                        )
                    ]
                    columns_sql = ", ".join(
                        f"`{field}`" for field in insert_fields
                    )
                    placeholders = ", ".join(
                        ["%s"] * len(insert_fields)
                    )
                    sql = (
                        f"INSERT INTO `{config['table']}` "
                        f"({columns_sql}) VALUES ({placeholders})"
                    )
                    params = tuple(values[field] for field in insert_fields)
                    cursor.execute(sql, params)
                    success_text = "Data berhasil ditambahkan."
                else:
                    update_fields = [field for field in fields if field != pk]
                    set_sql = ", ".join(
                        f"`{field}` = %s" for field in update_fields
                    )
                    sql = (
                        f"UPDATE `{config['table']}` SET {set_sql} "
                        f"WHERE `{pk}` = %s"
                    )
                    params = tuple(
                        values[field] for field in update_fields
                    ) + (selected["pk"],)
                    cursor.execute(sql, params)
                    success_text = "Data berhasil diperbarui."

                conn.commit()
                messagebox.showinfo("Berhasil", success_text)
                clear_form()
                load_data()

            except mysql.connector.Error as err:
                if conn and conn.is_connected():
                    conn.rollback()
                messagebox.showerror(
                    "Database Error",
                    f"Gagal menyimpan data:\n{err}"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        def delete_data():
            chosen = tree.selection()
            if not chosen:
                messagebox.showwarning(
                    "Pilih Data", "Pilih baris data yang ingin dihapus."
                )
                return

            values = tree.item(chosen[0], "values")
            pk_index = fields.index(config["pk"])
            pk_value = values[pk_index]

            if not messagebox.askyesno(
                "Konfirmasi Hapus",
                f"Yakin ingin menghapus data dengan "
                f"{config['pk']} = {pk_value}?"
            ):
                return

            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    f"DELETE FROM `{config['table']}` "
                    f"WHERE `{config['pk']}` = %s",
                    (pk_value,)
                )
                conn.commit()
                messagebox.showinfo("Berhasil", "Data berhasil dihapus.")
                clear_form()
                load_data()

            except mysql.connector.Error as err:
                if conn and conn.is_connected():
                    conn.rollback()
                messagebox.showerror(
                    "Database Error",
                    f"Gagal menghapus data:\n{err}"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        def make_action(text, command, color=PINK_MAIN):
            button = tk.Button(
                action_frame, text=text,
                font=("Segoe UI", 9, "bold"),
                bg=color, fg=WHITE,
                activebackground=PINK_HOVER,
                activeforeground=WHITE,
                relief="flat", cursor="hand2",
                command=command
            )
            button.pack(side="left", padx=(0, 7), ipadx=8, ipady=5)
            return button

        make_action("＋ Tambah / Simpan", save_data)
        make_action("✎ Data Baru / Batal", clear_form, color=MUTED)
        make_action("⌫ Hapus", delete_data, color=PINK_DARK)
        make_action("⟳ Refresh", load_data, color=TEXT)

        tree.bind("<<TreeviewSelect>>", select_row)
        load_data()

    # =====================================================
    # PENUTUP APLIKASI
    # =====================================================

    def close_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SiakadApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
