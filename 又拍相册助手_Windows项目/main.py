import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("又拍相册助手")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
