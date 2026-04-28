from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QDateEdit,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import QDate


class DialogTambah(QDialog):

    def __init__(self, parent=None, data_edit=None):
        super().__init__(parent)
        self.data_edit = data_edit
        
        if data_edit:
            self.setWindowTitle("Edit Transaksi")
        else:
            self.setWindowTitle("Tambah Transaksi Baru")
        
        self.setMinimumWidth(400)
        self.setup_ui()
        
        if data_edit:
            self.isi_data_edit()

    def setup_ui(self):
        layout_utama = QVBoxLayout()
        layout_form = QFormLayout()

        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setDisplayFormat("dd-MM-yyyy")
        layout_form.addRow("Tanggal:", self.input_tanggal)

        self.input_jenis = QComboBox()
        self.input_jenis.addItems(["Pemasukan", "Pengeluaran"])
        layout_form.addRow("Jenis:", self.input_jenis)

        self.input_kategori = QComboBox()
        self.input_kategori.setEditable(True)
        self.input_kategori.addItems([
            "Makan & Minum",
            "Transportasi", 
            "Belanja",
            "Hiburan",
            "Pendidikan",
            "Gaji",
            "Bonus",
            "Lainnya"
        ])
        layout_form.addRow("Kategori:", self.input_kategori)

        self.input_jumlah = QLineEdit()
        self.input_jumlah.setPlaceholderText("Contoh: 50000")
        layout_form.addRow("Jumlah (Rp):", self.input_jumlah)

        self.input_keterangan = QTextEdit()
        self.input_keterangan.setPlaceholderText("Tulis catatan di sini (opsional)")
        self.input_keterangan.setMaximumHeight(80)
        layout_form.addRow("Keterangan:", self.input_keterangan)

        layout_utama.addLayout(layout_form)

        layout_tombol = QHBoxLayout()
        
        self.tombol_simpan = QPushButton("💾 Simpan")
        self.tombol_simpan.setObjectName("tombolSimpan")
        
        self.tombol_batal = QPushButton("❌ Batal")
        self.tombol_batal.setObjectName("tombolBatal")
        
        layout_tombol.addWidget(self.tombol_simpan)
        layout_tombol.addWidget(self.tombol_batal)
        
        layout_utama.addLayout(layout_tombol)
        self.setLayout(layout_utama)

        self.tombol_simpan.clicked.connect(self.validasi_dan_simpan)
        self.tombol_batal.clicked.connect(self.reject)

    def isi_data_edit(self):
        tanggal = QDate.fromString(self.data_edit[1], "yyyy-MM-dd")
        self.input_tanggal.setDate(tanggal)
        
        index_jenis = self.input_jenis.findText(self.data_edit[3])
        if index_jenis >= 0:
            self.input_jenis.setCurrentIndex(index_jenis)
        
        self.input_kategori.setCurrentText(self.data_edit[2])
        self.input_jumlah.setText(str(int(self.data_edit[4])))
        
        if self.data_edit[5]:
            self.input_keterangan.setPlainText(self.data_edit[5])

    def validasi_dan_simpan(self):
        jumlah_text = self.input_jumlah.text().strip()
        if not jumlah_text:
            QMessageBox.warning(self, "Peringatan", "Jumlah tidak boleh kosong!")
            return
        
        try:
            jumlah = float(jumlah_text)
            if jumlah <= 0:
                QMessageBox.warning(self, "Peringatan", "Jumlah harus lebih dari 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Jumlah harus berupa angka!")
            return
        
        self.accept()

    def ambil_data(self):
        data = {
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "kategori": self.input_kategori.currentText(),
            "jenis": self.input_jenis.currentText(),
            "jumlah": float(self.input_jumlah.text()),
            "keterangan": self.input_keterangan.toPlainText().strip(),
        }
        return data
