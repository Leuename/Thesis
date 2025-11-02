import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from backend import SplashScreen

app = QApplication(sys.argv)

window = SplashScreen()

window.show()
app.exec()