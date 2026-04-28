import sqlite3


class Database:

    def __init__(self):
        self.koneksi = sqlite3.connect("keuangan.db")
        self.cursor = self.koneksi.cursor()
        self.buat_tabel()

    def buat_tabel(self):
        perintah_sql = """
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                kategori TEXT NOT NULL,
                jenis TEXT NOT NULL,
                jumlah REAL NOT NULL,
                keterangan TEXT
            )
        """
        self.cursor.execute(perintah_sql)
        self.koneksi.commit()

    def tambah_transaksi(self, tanggal, kategori, jenis, jumlah, keterangan):
        perintah_sql = """
            INSERT INTO transaksi (tanggal, kategori, jenis, jumlah, keterangan)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(perintah_sql, (tanggal, kategori, jenis, jumlah, keterangan))
        self.koneksi.commit()

    def ambil_semua_transaksi(self):
        perintah_sql = "SELECT * FROM transaksi ORDER BY tanggal DESC"
        self.cursor.execute(perintah_sql)
        return self.cursor.fetchall()

    def update_transaksi(self, id_transaksi, tanggal, kategori, jenis, jumlah, keterangan):
        perintah_sql = """
            UPDATE transaksi 
            SET tanggal = ?, kategori = ?, jenis = ?, jumlah = ?, keterangan = ?
            WHERE id = ?
        """
        self.cursor.execute(perintah_sql, (tanggal, kategori, jenis, jumlah, keterangan, id_transaksi))
        self.koneksi.commit()

    def hapus_transaksi(self, id_transaksi):
        perintah_sql = "DELETE FROM transaksi WHERE id = ?"
        self.cursor.execute(perintah_sql, (id_transaksi,))
        self.koneksi.commit()

    def hitung_total(self):
        self.cursor.execute(
            "SELECT COALESCE(SUM(jumlah), 0) FROM transaksi WHERE jenis = 'Pemasukan'"
        )
        total_pemasukan = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COALESCE(SUM(jumlah), 0) FROM transaksi WHERE jenis = 'Pengeluaran'"
        )
        total_pengeluaran = self.cursor.fetchone()[0]

        return total_pemasukan, total_pengeluaran

    def tutup_koneksi(self):
        self.koneksi.close()
