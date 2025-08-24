from ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QListWidgetItem
import sys
from camera_ui import MySideBar

app = QApplication(sys.argv)

window = MySideBar()

window.show()
app.exec()
