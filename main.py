import sys
import os

from PySide6.QtWidgets import QApplication
from main_window import MainWindow


def muat_stylesheet(app):
    path_qss = os.path.join(os.path.dirname(__file__), "style.qss")
    
    if os.path.exists(path_qss):
        with open(path_qss, "r") as file:
            style = file.read()
            app.setStyleSheet(style)
        print("✅ Style QSS berhasil dimuat!")
    else:
        print("⚠️  File style.qss tidak ditemukan. Menggunakan tampilan default.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    muat_stylesheet(app)

    jendela = MainWindow()
    jendela.show()

    sys.exit(app.exec())
