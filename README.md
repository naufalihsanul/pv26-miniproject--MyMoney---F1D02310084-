# 💰 MyMoney - Pencatat Keuangan Pribadi

Aplikasi desktop sederhana untuk mencatat pemasukan dan pengeluaran harian, dibuat menggunakan **PySide6** dan **SQLite**.

## 📋 Deskripsi

MyMoney adalah aplikasi pencatat keuangan pribadi yang memungkinkan pengguna untuk:
- Menambah, mengedit, dan menghapus transaksi keuangan
- Melihat ringkasan pemasukan, pengeluaran, dan saldo
- Mengkategorikan transaksi (Makan, Transport, Gaji, dll)
- Menyimpan data secara persisten menggunakan database SQLite

## 🛠️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|-----------|--------|
| Python 3 | Bahasa pemrograman utama |
| PySide6 | Framework GUI (antarmuka grafis) |
| SQLite | Database lokal untuk penyimpanan data |
| QSS | Styling tampilan (mirip CSS) |

## 📁 Struktur Project nya

```
UTS_PEMVIS/
├── main.py            # Entry point aplikasi
├── database.py        # Operasi database (CRUD)
├── main_window.py     # Tampilan jendela utama
├── dialog_tambah.py   # Dialog form tambah/edit
├── style.qss          # File styling eksternal
├── HASIL/             # Folder screenshot hasil aplikasi
└── README.md          # Dokumentasi ini
```

## 🚀 Cara Menjalankan

1. Pastikan Python 3 sudah terinstall
2. Install PySide6:
   ```
   pip install PySide6
   ```
3. Jalankan aplikasi:
   ```
   python main.py
   ```

## 📸 Hasil Tampilan Aplikasi

Berikut adalah beberapa tangkapan layar (screenshot) dari aplikasi MyMoney:

### Screenshot 1
![Screenshot 1](HASIL/Screenshot%202026-04-28%20163242.png)

### Screenshot 2
![Screenshot 2](HASIL/Screenshot%202026-04-28%20163322.png)

### Screenshot 3
![Screenshot 3](HASIL/Screenshot%202026-04-28%20163404.png)

### Screenshot 4
![Screenshot 4](HASIL/Screenshot%202026-04-28%20163452.png)

### Screenshot 5
![Screenshot 5](HASIL/Screenshot%202026-04-28%20163512.png)

## 👤 Informasi Mahasiswa

- **Nama:** Naufal Ihsanul Islam
- **NIM:** F1D02310084
- **Kelas:** C
- **Mata Kuliah:** Pemrograman Visual
