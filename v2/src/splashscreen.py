from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import resources


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 770)
        MainWindow.setMinimumSize(QSize(1280, 770))
        MainWindow.setMaximumSize(QSize(1280, 770))
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(-10, 40, 1321, 741))
        self.frame_3.setStyleSheet(u"#frame_3{\n"
"\tborder:none;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_1 = QWidget(self.frame_3)
        self.widget_1.setObjectName(u"widget_1")
        self.verticalLayout = QVBoxLayout(self.widget_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.icon = QLabel(self.widget_1)
        self.icon.setObjectName(u"icon")
        self.icon.setPixmap(QPixmap(u":/420(1).png"))
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.icon)

        self.ivis = QLabel(self.widget_1)
        self.ivis.setObjectName(u"ivis")
        font = QFont()
        font.setFamilies([u"Poppins"])
        font.setPointSize(60)
        font.setBold(True)
        self.ivis.setFont(font)
        self.ivis.setStyleSheet(u"color: #27296c;")
        self.ivis.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ivis)
        self.ivis.move(self.ivis.x(), self.ivis.y() + 300)  # Increase 50 as needed for more downward movement

        self.ivis_word = QLabel(self.widget_1)
        self.ivis_word.setObjectName(u"ivis_word")
        self.ivis_word.setMinimumSize(QSize(653, 44))
        self.ivis_word.setMaximumSize(QSize(1000, 44))
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.ivis_word.setFont(font1)
        self.ivis_word.setStyleSheet(u"color: #27296c;")
        self.ivis_word.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ivis_word)

        self.quote = QLabel(self.widget_1)
        self.quote.setObjectName(u"quote")
        self.quote.setMinimumSize(QSize(653, 28))
        self.quote.setMaximumSize(QSize(1000, 28))
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(True)
        self.quote.setFont(font2)
        self.quote.setStyleSheet(u"color: #27296c;")
        self.quote.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.quote)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout.addWidget(self.widget_1, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.frame_3)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(1300, 40))
        self.widget_2.setMaximumSize(QSize(1300, 45))
        self.widget_2.setStyleSheet(u"background-color: #27296c;")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setBold(True)
        font3.setItalic(False)
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color: white;")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.horizontalSpacer = QSpacerItem(800, 19, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font3)
        self.label_7.setStyleSheet(u"color: white;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(30, 20, 240, 71))
        self.label_6.setPixmap(QPixmap(u":/240.png"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        # -----------------------
        # Animation (all fade in, sequential)
        # -----------------------

        # Setup QGraphicsOpacityEffects for all widgets
        self._icon_opacity = QGraphicsOpacityEffect(self.icon)
        self.icon.setGraphicsEffect(self._icon_opacity)
        self._icon_opacity.setOpacity(0.0)

        self._ivis_opacity = QGraphicsOpacityEffect(self.ivis)
        self.ivis.setGraphicsEffect(self._ivis_opacity)
        self._ivis_opacity.setOpacity(0.0)

        self._ivis_word_opacity = QGraphicsOpacityEffect(self.ivis_word)
        self.ivis_word.setGraphicsEffect(self._ivis_word_opacity)
        self._ivis_word_opacity.setOpacity(0.0)

        self._quote_opacity = QGraphicsOpacityEffect(self.quote)
        self.quote.setGraphicsEffect(self._quote_opacity)
        self._quote_opacity.setOpacity(0.0)

        # Animations for fade in
        self.icon_fade_in = QPropertyAnimation(self._icon_opacity, b"opacity")
        self.icon_fade_in.setDuration(800)
        self.icon_fade_in.setStartValue(0.0)
        self.icon_fade_in.setEndValue(1.0)

        self.ivis_fade_in = QPropertyAnimation(self._ivis_opacity, b"opacity")
        self.ivis_fade_in.setDuration(500)
        self.ivis_fade_in.setStartValue(0.0)
        self.ivis_fade_in.setEndValue(1.0)

        self.ivis_word_fade = QPropertyAnimation(self._ivis_word_opacity, b"opacity")
        self.ivis_word_fade.setDuration(300)
        self.ivis_word_fade.setStartValue(0.0)
        self.ivis_word_fade.setEndValue(1.0)

        self.quote_fade = QPropertyAnimation(self._quote_opacity, b"opacity")
        self.quote_fade.setDuration(800)
        self.quote_fade.setStartValue(0.0)
        self.quote_fade.setEndValue(1.0)

        # Fade sequence: icon → ivis → ivis_word → quote
        def start_ivis_fade():
            self.ivis_fade_in.start()

        def start_ivis_word_fade():
            self.ivis_word_fade.start()

        def start_quote_fade():
            self.quote_fade.start()

        self.icon_fade_in.finished.connect(start_ivis_fade)
        self.ivis_fade_in.finished.connect(start_ivis_word_fade)
        self.ivis_word_fade.finished.connect(start_quote_fade)

        # Flag splash as done when quote fade completes
        def on_all_done():
            app = QApplication.instance()
            setattr(app, 'splash_done', True)

        self.quote_fade.finished.connect(on_all_done)

        # Start the sequence on window show
        QTimer.singleShot(60, lambda: self.icon_fade_in.start())


    # setupUi


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.icon.setText("")
        self.ivis.setText(QCoreApplication.translate("MainWindow", u"IVIS", None))
        self.ivis_word.setText(QCoreApplication.translate("MainWindow", u"                                         Intelligent Visual Inspection System", None))
        self.quote.setText(QCoreApplication.translate("MainWindow", u"                                                        Empowering Semiconductor Quality through Intelligent Detection", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Developed by FJMM for Fastech Synergy Philippines, Inc.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"                \u00a9 2025", None))
        self.label_6.setText("")
    # retranslateUi



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.splash_done = False
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Simple poller to close splash when done (the app should handle transition to main window)
    def check_and_close():
        if getattr(app, 'splash_done', False):
            # here we close the splash window — replace with showing your real main window
            MainWindow.close()
            poller.stop()

    poller = QTimer()
    poller.timeout.connect(check_and_close)
    poller.start(120)

    sys.exit(app.exec())
