from ui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QListWidgetItem
import sys
from camera_ui import CameraUI

app = QApplication(sys.argv)

window = CameraUI()

window.show()
app.exec()
