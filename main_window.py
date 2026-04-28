from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QMessageBox,
    QHeaderView,
    QMenuBar,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from database import Database
from dialog_tambah import DialogTambah


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("💰 MyMoney - Pencatat Keuangan Pribadi")
        self.setMinimumSize(800, 550)

        self.db = Database()

        self.setup_menu_bar()
        self.setup_ui()

        self.muat_data()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        menu_aplikasi = menu_bar.addMenu("📋 Aplikasi")

        aksi_tentang = QAction("Tentang Aplikasi", self)
        aksi_tentang.triggered.connect(self.tampilkan_tentang)
        menu_aplikasi.addAction(aksi_tentang)

    def setup_ui(self):
        widget_pusat = QWidget()
        self.setCentralWidget(widget_pusat)

        layout_utama = QVBoxLayout()
        layout_utama.setSpacing(10)
        layout_utama.setContentsMargins(20, 20, 20, 20)

        self.label_identitas = QLabel("👤 Naufal Ihsanul Islam | NIM: F1D02310084")
        self.label_identitas.setObjectName("labelIdentitas")
        self.label_identitas.setAlignment(Qt.AlignCenter)
        layout_utama.addWidget(self.label_identitas)

        self.label_judul = QLabel("💰 MyMoney - Pencatat Keuangan Pribadi")
        self.label_judul.setObjectName("labelJudul")
        self.label_judul.setAlignment(Qt.AlignCenter)
        layout_utama.addWidget(self.label_judul)

        layout_ringkasan = QHBoxLayout()

        self.label_pemasukan = QLabel("Pemasukan: Rp 0")
        self.label_pemasukan.setObjectName("labelPemasukan")
        self.label_pemasukan.setAlignment(Qt.AlignCenter)

        self.label_pengeluaran = QLabel("Pengeluaran: Rp 0")
        self.label_pengeluaran.setObjectName("labelPengeluaran")
        self.label_pengeluaran.setAlignment(Qt.AlignCenter)

        self.label_saldo = QLabel("Saldo: Rp 0")
        self.label_saldo.setObjectName("labelSaldo")
        self.label_saldo.setAlignment(Qt.AlignCenter)

        layout_ringkasan.addWidget(self.label_pemasukan)
        layout_ringkasan.addWidget(self.label_pengeluaran)
        layout_ringkasan.addWidget(self.label_saldo)

        layout_utama.addLayout(layout_ringkasan)

        self.tabel = QTableWidget()
        self.tabel.setColumnCount(6)
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Kategori", "Jenis", "Jumlah (Rp)", "Keterangan"
        ])
        
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        
        self.tabel.setColumnWidth(0, 50)
        self.tabel.setColumnWidth(1, 110)
        self.tabel.setColumnWidth(2, 130)
        self.tabel.setColumnWidth(3, 110)
        self.tabel.setColumnWidth(4, 120)

        self.tabel.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabel.setEditTriggers(QTableWidget.NoEditTriggers)

        layout_utama.addWidget(self.tabel)

        layout_tombol = QHBoxLayout()

        self.tombol_tambah = QPushButton("➕ Tambah")
        self.tombol_tambah.setObjectName("tombolTambah")

        self.tombol_edit = QPushButton("✏️ Edit")
        self.tombol_edit.setObjectName("tombolEdit")

        self.tombol_hapus = QPushButton("🗑️ Hapus")
        self.tombol_hapus.setObjectName("tombolHapus")

        layout_tombol.addWidget(self.tombol_tambah)
        layout_tombol.addWidget(self.tombol_edit)
        layout_tombol.addWidget(self.tombol_hapus)

        layout_utama.addLayout(layout_tombol)

        widget_pusat.setLayout(layout_utama)

        self.tombol_tambah.clicked.connect(self.buka_dialog_tambah)
        self.tombol_edit.clicked.connect(self.buka_dialog_edit)
        self.tombol_hapus.clicked.connect(self.hapus_data)

    def muat_data(self):
        data_list = self.db.ambil_semua_transaksi()
        self.tabel.setRowCount(len(data_list))

        for baris, data in enumerate(data_list):
            for kolom in range(6):
                if kolom == 4:
                    teks = f"{int(data[kolom]):,}".replace(",", ".")
                else:
                    teks = str(data[kolom]) if data[kolom] else ""
                
                item = QTableWidgetItem(teks)
                item.setTextAlignment(Qt.AlignCenter)
                self.tabel.setItem(baris, kolom, item)

        self.perbarui_ringkasan()

    def perbarui_ringkasan(self):
        pemasukan, pengeluaran = self.db.hitung_total()
        saldo = pemasukan - pengeluaran

        self.label_pemasukan.setText(
            f"📈 Pemasukan: Rp {int(pemasukan):,}".replace(",", ".")
        )
        self.label_pengeluaran.setText(
            f"📉 Pengeluaran: Rp {int(pengeluaran):,}".replace(",", ".")
        )
        self.label_saldo.setText(
            f"💰 Saldo: Rp {int(saldo):,}".replace(",", ".")
        )

    def buka_dialog_tambah(self):
        dialog = DialogTambah(parent=self)
        
        if dialog.exec():
            data = dialog.ambil_data()
            self.db.tambah_transaksi(
                data["tanggal"],
                data["kategori"],
                data["jenis"],
                data["jumlah"],
                data["keterangan"],
            )
            self.muat_data()

    def buka_dialog_edit(self):
        baris_terpilih = self.tabel.currentRow()
        if baris_terpilih < 0:
            QMessageBox.warning(
                self, "Peringatan", "Pilih data yang ingin diedit terlebih dahulu!"
            )
            return

        id_transaksi = int(self.tabel.item(baris_terpilih, 0).text())
        tanggal = self.tabel.item(baris_terpilih, 1).text()
        kategori = self.tabel.item(baris_terpilih, 2).text()
        jenis = self.tabel.item(baris_terpilih, 3).text()
        jumlah_text = self.tabel.item(baris_terpilih, 4).text().replace(".", "")
        jumlah = float(jumlah_text)
        keterangan = self.tabel.item(baris_terpilih, 5).text()

        data_lama = (id_transaksi, tanggal, kategori, jenis, jumlah, keterangan)

        dialog = DialogTambah(parent=self, data_edit=data_lama)
        
        if dialog.exec():
            data_baru = dialog.ambil_data()
            self.db.update_transaksi(
                id_transaksi,
                data_baru["tanggal"],
                data_baru["kategori"],
                data_baru["jenis"],
                data_baru["jumlah"],
                data_baru["keterangan"],
            )
            self.muat_data()

    def hapus_data(self):
        baris_terpilih = self.tabel.currentRow()
        if baris_terpilih < 0:
            QMessageBox.warning(
                self, "Peringatan", "Pilih data yang ingin dihapus terlebih dahulu!"
            )
            return

        id_transaksi = int(self.tabel.item(baris_terpilih, 0).text())
        kategori = self.tabel.item(baris_terpilih, 2).text()
        jumlah = self.tabel.item(baris_terpilih, 4).text()

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus transaksi:\n"
            f"Kategori: {kategori}\n"
            f"Jumlah: Rp {jumlah}\n\n"
            f"Data yang dihapus tidak dapat dikembalikan!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            self.db.hapus_transaksi(id_transaksi)
            self.muat_data()

    def tampilkan_tentang(self):
        QMessageBox.about(
            self,
            "Tentang Aplikasi",
            "<h2>💰 MyMoney</h2>"
            "<p><b>Pencatat Keuangan Pribadi</b></p>"
            "<hr>"
            "<p>Aplikasi sederhana untuk mencatat pemasukan dan "
            "pengeluaran harian menggunakan PySide6 dan SQLite.</p>"
            "<br>"
            "<p><b>Dibuat oleh:</b></p>"
            "<p>Nama: Naufal Ihsanul Islam<br>"
            "NIM: F1D02310084<br>"
            "Kelas: C<br>"
            "Mata Kuliah: Pemrograman Visual</p>"
        )

    def closeEvent(self, event):
        self.db.tutup_koneksi()
        event.accept()
