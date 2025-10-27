
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1580, 947)
        MainWindow.setMinimumSize(QSize(1580, 947))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/GUI FORMAT.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(1580, 947))
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(830, 600))
        self.widget.setMaximumSize(QSize(830, 600))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.live_camera = QLabel(self.widget)
        self.live_camera.setObjectName(u"live_camera")
        self.live_camera.setMinimumSize(QSize(830, 600))
        self.live_camera.setMaximumSize(QSize(830, 600))
        self.live_camera.setStyleSheet(u"QLabel {\n"
"    border: 2px solid black;      /* thickness, style, and color */\n"
"    border-radius: 5px;           /* optional: rounded corners */\n"
"    padding: 5px;                 /* optional: inner spacing */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.live_camera, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        self.camera = QWidget(self.frame)
        self.camera.setObjectName(u"camera")
        self.camera.setMinimumSize(QSize(720, 890))
        self.camera.setMaximumSize(QSize(720, 890))
        self.camera.setStyleSheet(u"#camera{\n"
"	border:none;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.camera)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.odd_camera = QWidget(self.camera)
        self.odd_camera.setObjectName(u"odd_camera")
        self.odd_camera.setMinimumSize(QSize(350, 890))
        self.odd_camera.setMaximumSize(QSize(350, 890))
        self.odd_camera.setStyleSheet(u"#cam2{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam4{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam6{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam8{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam10{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam1{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam3{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam5{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam7{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam9{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#camera_widget_2{\n"
"	border:none;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.odd_camera)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 9, 0, 0)
        self.cam1 = QWidget(self.odd_camera)
        self.cam1.setObjectName(u"cam1")
        self.cam1.setMinimumSize(QSize(350, 160))
        self.cam1.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_62 = QHBoxLayout(self.cam1)
        self.horizontalLayout_62.setSpacing(0)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(0, 0, 0, 0)
        self.image_1 = QLabel(self.cam1)
        self.image_1.setObjectName(u"image_1")
        self.image_1.setMinimumSize(QSize(175, 160))
        self.image_1.setMaximumSize(QSize(175, 160))
        font = QFont()
        font.setFamilies([u"Poppins"])
        self.image_1.setFont(font)
        self.image_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_62.addWidget(self.image_1)

        self.image_1_description = QLabel(self.cam1)
        self.image_1_description.setObjectName(u"image_1_description")
        self.image_1_description.setMinimumSize(QSize(0, 160))
        self.image_1_description.setMaximumSize(QSize(16777215, 160))
        self.image_1_description.setFont(font)

        self.horizontalLayout_62.addWidget(self.image_1_description)


        self.verticalLayout_4.addWidget(self.cam1)

        self.cam3 = QWidget(self.odd_camera)
        self.cam3.setObjectName(u"cam3")
        self.cam3.setMinimumSize(QSize(350, 160))
        self.cam3.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_63 = QHBoxLayout(self.cam3)
        self.horizontalLayout_63.setSpacing(0)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.image_3 = QLabel(self.cam3)
        self.image_3.setObjectName(u"image_3")
        self.image_3.setMinimumSize(QSize(175, 160))
        self.image_3.setMaximumSize(QSize(175, 160))
        self.image_3.setFont(font)

        self.horizontalLayout_63.addWidget(self.image_3)

        self.image_3_description = QLabel(self.cam3)
        self.image_3_description.setObjectName(u"image_3_description")
        self.image_3_description.setMinimumSize(QSize(0, 160))
        self.image_3_description.setMaximumSize(QSize(16777215, 160))
        self.image_3_description.setFont(font)

        self.horizontalLayout_63.addWidget(self.image_3_description)


        self.verticalLayout_4.addWidget(self.cam3)

        self.cam5 = QWidget(self.odd_camera)
        self.cam5.setObjectName(u"cam5")
        self.cam5.setMinimumSize(QSize(350, 160))
        self.cam5.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_64 = QHBoxLayout(self.cam5)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.image_5 = QLabel(self.cam5)
        self.image_5.setObjectName(u"image_5")
        self.image_5.setMinimumSize(QSize(175, 160))
        self.image_5.setMaximumSize(QSize(175, 160))
        self.image_5.setFont(font)

        self.horizontalLayout_64.addWidget(self.image_5)

        self.image_5_description = QLabel(self.cam5)
        self.image_5_description.setObjectName(u"image_5_description")
        self.image_5_description.setMinimumSize(QSize(0, 160))
        self.image_5_description.setMaximumSize(QSize(16777215, 160))
        self.image_5_description.setFont(font)

        self.horizontalLayout_64.addWidget(self.image_5_description)


        self.verticalLayout_4.addWidget(self.cam5)

        self.cam7 = QWidget(self.odd_camera)
        self.cam7.setObjectName(u"cam7")
        self.cam7.setMinimumSize(QSize(350, 160))
        self.cam7.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_65 = QHBoxLayout(self.cam7)
        self.horizontalLayout_65.setSpacing(0)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.image_7 = QLabel(self.cam7)
        self.image_7.setObjectName(u"image_7")
        self.image_7.setMinimumSize(QSize(175, 160))
        self.image_7.setMaximumSize(QSize(175, 160))
        self.image_7.setFont(font)

        self.horizontalLayout_65.addWidget(self.image_7)

        self.image_7_description = QLabel(self.cam7)
        self.image_7_description.setObjectName(u"image_7_description")
        self.image_7_description.setMinimumSize(QSize(0, 160))
        self.image_7_description.setMaximumSize(QSize(16777215, 160))
        self.image_7_description.setFont(font)

        self.horizontalLayout_65.addWidget(self.image_7_description)


        self.verticalLayout_4.addWidget(self.cam7)

        self.cam9 = QWidget(self.odd_camera)
        self.cam9.setObjectName(u"cam9")
        self.cam9.setMinimumSize(QSize(350, 160))
        self.cam9.setMaximumSize(QSize(350, 160))
        self.cam9.setFont(font)
        self.horizontalLayout_66 = QHBoxLayout(self.cam9)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.image_9 = QLabel(self.cam9)
        self.image_9.setObjectName(u"image_9")
        self.image_9.setMinimumSize(QSize(175, 160))
        self.image_9.setMaximumSize(QSize(175, 160))
        self.image_9.setFont(font)

        self.horizontalLayout_66.addWidget(self.image_9)

        self.image_9_description = QLabel(self.cam9)
        self.image_9_description.setObjectName(u"image_9_description")
        self.image_9_description.setFont(font)

        self.horizontalLayout_66.addWidget(self.image_9_description)


        self.verticalLayout_4.addWidget(self.cam9)


        self.horizontalLayout.addWidget(self.odd_camera)

        self.even_camera = QWidget(self.camera)
        self.even_camera.setObjectName(u"even_camera")
        self.even_camera.setMinimumSize(QSize(350, 890))
        self.even_camera.setMaximumSize(QSize(350, 890))
        self.even_camera.setStyleSheet(u"#cam2{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam4{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam6{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam8{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#cam10{\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"#camera_widget_1{\n"
"	border:none;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.even_camera)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.cam2 = QWidget(self.even_camera)
        self.cam2.setObjectName(u"cam2")
        self.cam2.setMinimumSize(QSize(350, 160))
        self.cam2.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_52 = QHBoxLayout(self.cam2)
        self.horizontalLayout_52.setSpacing(0)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.image_2 = QLabel(self.cam2)
        self.image_2.setObjectName(u"image_2")
        self.image_2.setMinimumSize(QSize(160, 160))
        self.image_2.setMaximumSize(QSize(160, 160))
        self.image_2.setFont(font)

        self.horizontalLayout_52.addWidget(self.image_2)

        self.image_2_description = QLabel(self.cam2)
        self.image_2_description.setObjectName(u"image_2_description")
        self.image_2_description.setFont(font)

        self.horizontalLayout_52.addWidget(self.image_2_description)


        self.verticalLayout_2.addWidget(self.cam2)

        self.cam4 = QWidget(self.even_camera)
        self.cam4.setObjectName(u"cam4")
        self.cam4.setMinimumSize(QSize(350, 160))
        self.cam4.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_53 = QHBoxLayout(self.cam4)
        self.horizontalLayout_53.setSpacing(0)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.horizontalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.image_4 = QLabel(self.cam4)
        self.image_4.setObjectName(u"image_4")
        self.image_4.setMinimumSize(QSize(175, 160))
        self.image_4.setMaximumSize(QSize(175, 160))
        self.image_4.setFont(font)

        self.horizontalLayout_53.addWidget(self.image_4)

        self.image_4_description = QLabel(self.cam4)
        self.image_4_description.setObjectName(u"image_4_description")
        self.image_4_description.setMinimumSize(QSize(0, 160))
        self.image_4_description.setMaximumSize(QSize(16777215, 160))
        self.image_4_description.setFont(font)

        self.horizontalLayout_53.addWidget(self.image_4_description)


        self.verticalLayout_2.addWidget(self.cam4)

        self.cam6 = QWidget(self.even_camera)
        self.cam6.setObjectName(u"cam6")
        self.cam6.setMinimumSize(QSize(350, 160))
        self.cam6.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_54 = QHBoxLayout(self.cam6)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.horizontalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.image_6 = QLabel(self.cam6)
        self.image_6.setObjectName(u"image_6")
        self.image_6.setMinimumSize(QSize(175, 160))
        self.image_6.setMaximumSize(QSize(175, 160))
        self.image_6.setFont(font)

        self.horizontalLayout_54.addWidget(self.image_6)

        self.image_6_description = QLabel(self.cam6)
        self.image_6_description.setObjectName(u"image_6_description")
        self.image_6_description.setFont(font)

        self.horizontalLayout_54.addWidget(self.image_6_description)


        self.verticalLayout_2.addWidget(self.cam6)

        self.cam8 = QWidget(self.even_camera)
        self.cam8.setObjectName(u"cam8")
        self.cam8.setMinimumSize(QSize(350, 160))
        self.cam8.setMaximumSize(QSize(350, 160))
        self.horizontalLayout_55 = QHBoxLayout(self.cam8)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.image_8 = QLabel(self.cam8)
        self.image_8.setObjectName(u"image_8")
        self.image_8.setMinimumSize(QSize(175, 160))
        self.image_8.setMaximumSize(QSize(175, 160))
        self.image_8.setFont(font)

        self.horizontalLayout_55.addWidget(self.image_8)

        self.image_8_description = QLabel(self.cam8)
        self.image_8_description.setObjectName(u"image_8_description")
        self.image_8_description.setMinimumSize(QSize(0, 160))
        self.image_8_description.setMaximumSize(QSize(16777215, 160))
        self.image_8_description.setFont(font)

        self.horizontalLayout_55.addWidget(self.image_8_description)


        self.verticalLayout_2.addWidget(self.cam8)

        self.cam10 = QWidget(self.even_camera)
        self.cam10.setObjectName(u"cam10")
        self.cam10.setMinimumSize(QSize(350, 160))
        self.cam10.setMaximumSize(QSize(350, 160))
        self.cam10.setFont(font)
        self.horizontalLayout_56 = QHBoxLayout(self.cam10)
        self.horizontalLayout_56.setSpacing(0)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.image_10 = QLabel(self.cam10)
        self.image_10.setObjectName(u"image_10")
        self.image_10.setMinimumSize(QSize(175, 175))
        self.image_10.setMaximumSize(QSize(175, 175))
        self.image_10.setFont(font)

        self.horizontalLayout_56.addWidget(self.image_10)

        self.image_10_description = QLabel(self.cam10)
        self.image_10_description.setObjectName(u"image_10_description")
        self.image_10_description.setFont(font)

        self.horizontalLayout_56.addWidget(self.image_10_description)


        self.verticalLayout_2.addWidget(self.cam10)


        self.horizontalLayout.addWidget(self.even_camera)


        self.gridLayout_2.addWidget(self.camera, 0, 1, 3, 1)

        self.ini_frame = QFrame(self.frame)
        self.ini_frame.setObjectName(u"ini_frame")
        self.ini_frame.setMinimumSize(QSize(830, 0))
        self.ini_frame.setMaximumSize(QSize(830, 80))
        self.ini_frame.setStyleSheet(u"#ini_frame{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"	border-top:5px solid #27296c;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.ini_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ini_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.ini_frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.widget_7 = QWidget(self.ini_frame)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setStyleSheet(u"border:none;")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.action_button = QPushButton(self.widget_7)
        self.action_button.setObjectName(u"action_button")
        self.action_button.setMinimumSize(QSize(41, 41))
        self.action_button.setMaximumSize(QSize(41, 41))
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(20)
        self.action_button.setFont(font1)
        self.action_button.setStyleSheet(u"border:none;")
        icon1 = QIcon()
        icon1.addFile(u":/play.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/pause.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        icon1.addFile(u":/pause.png", QSize(), QIcon.Mode.Active, QIcon.State.On)
        self.action_button.setIcon(icon1)
        self.action_button.setIconSize(QSize(32, 32))
        self.action_button.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.action_button)


        self.horizontalLayout_7.addWidget(self.widget_7)

        self.widget_9 = QWidget(self.ini_frame)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setStyleSheet(u"border:none;")
        self.verticalLayout_3 = QVBoxLayout(self.widget_9)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(100, 0, 0, 0)
        self.wire_combo = QComboBox(self.widget_9)
        icon2 = QIcon()
        icon2.addFile(u":/wires.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.wire_combo.addItem(icon2, "")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.addItem("")
        self.wire_combo.setObjectName(u"wire_combo")
        self.wire_combo.setMinimumSize(QSize(71, 51))
        self.wire_combo.setMaximumSize(QSize(71, 51))
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(12)
        self.wire_combo.setFont(font2)
        self.wire_combo.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.wire_combo.setStyleSheet(u"QComboBox::drop-down {\n"
"    border: 0px;\n"
"	width:0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"QComboBox {\n"
"    padding-left: 20px;\n"
"	border:none;\n"
"}\n"
"")
        self.wire_combo.setEditable(False)
        self.wire_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.wire_combo.setIconSize(QSize(32, 32))
        self.wire_combo.setFrame(True)

        self.verticalLayout_3.addWidget(self.wire_combo)


        self.horizontalLayout_7.addWidget(self.widget_9)

        self.widget_8 = QWidget(self.ini_frame)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setStyleSheet(u"border:none;")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.export_button = QPushButton(self.widget_8)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setMinimumSize(QSize(51, 41))
        self.export_button.setMaximumSize(QSize(51, 41))
        self.export_button.setFont(font1)
        self.export_button.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-top: 8px;\n"
"    padding-bottom: 5px;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/export.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.export_button.setIcon(icon3)
        self.export_button.setIconSize(QSize(46, 46))
        self.export_button.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.export_button)


        self.horizontalLayout_7.addWidget(self.widget_8)


        self.gridLayout_2.addWidget(self.ini_frame, 1, 0, 1, 1)

        self.strip = QWidget(self.frame)
        self.strip.setObjectName(u"strip")
        self.strip.setMinimumSize(QSize(830, 180))
        self.strip.setMaximumSize(QSize(830, 180))
        self.strip.setStyleSheet(u"#strip{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"    border-top: none;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.strip)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.current_qlabel = QLabel(self.strip)
        self.current_qlabel.setObjectName(u"current_qlabel")
        self.current_qlabel.setMinimumSize(QSize(830, 40))
        self.current_qlabel.setMaximumSize(QSize(830, 50))
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setPointSize(14)
        font3.setBold(True)
        self.current_qlabel.setFont(font3)
        self.current_qlabel.setStyleSheet(u"#current_qlabel {\n"
"        background-color: #27296c;   /* dark blue header */\n"
"        color: white;\n"
"        font-weight: bold;\n"
"        font-size: 14pt;\n"
"        padding: 6px 10px;\n"
"        border: none;\n"
"        border-bottom: none;         /* so it merges with frame */\n"
"        border-top-left-radius: 1px;\n"
"        border-top-right-radius: 1px;\n"
"		border-radius:60px;\n"
"}\n"
"\n")

        
        self.verticalLayout.addWidget(self.current_qlabel)

        self.widget_20 = QWidget(self.strip)
        self.widget_20.setObjectName(u"widget_20")
        self.widget_20.setMinimumSize(QSize(0, 0))
        self.widget_20.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_7 = QGridLayout(self.widget_20)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.widget_65 = QWidget(self.widget_20)
        self.widget_65.setObjectName(u"widget_65")
        self.widget_65.setMinimumSize(QSize(0, 0))
        self.widget_65.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_11 = QVBoxLayout(self.widget_65)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.widget_66 = QWidget(self.widget_65)
        self.widget_66.setObjectName(u"widget_66")
        self.widget_66.setMinimumSize(QSize(0, 0))
        self.widget_66.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_24 = QHBoxLayout(self.widget_66)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, 0, 0)
        self.label_71 = QLabel(self.widget_66)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setMinimumSize(QSize(61, 30))
        self.label_71.setMaximumSize(QSize(61, 30))
        font4 = QFont()
        font4.setFamilies([u"Poppins"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.label_71.setFont(font4)

        self.horizontalLayout_24.addWidget(self.label_71)

        self.magazine_to = QLineEdit(self.widget_66)
        self.magazine_to.setObjectName(u"magazine_to")
        self.magazine_to.setMinimumSize(QSize(328, 30))
        self.magazine_to.setMaximumSize(QSize(328, 30))
        self.magazine_to.setFont(font2)

        self.horizontalLayout_24.addWidget(self.magazine_to)


        self.verticalLayout_11.addWidget(self.widget_66)

        self.widget_67 = QWidget(self.widget_65)
        self.widget_67.setObjectName(u"widget_67")
        self.widget_67.setMinimumSize(QSize(0, 0))
        self.widget_67.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_25 = QHBoxLayout(self.widget_67)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, 0, 0)
        self.label_72 = QLabel(self.widget_67)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setMinimumSize(QSize(85, 30))
        self.label_72.setMaximumSize(QSize(85, 30))
        self.label_72.setFont(font4)

        self.horizontalLayout_25.addWidget(self.label_72)

        self.bad_unit_label = QLabel(self.widget_67)
        self.bad_unit_label.setObjectName(u"bad_unit_label")
        self.bad_unit_label.setMinimumSize(QSize(304, 30))
        self.bad_unit_label.setMaximumSize(QSize(304, 30))
        self.bad_unit_label.setFont(font2)
        self.bad_unit_label.setMargin(-1)
        self.bad_unit_label.setIndent(-3)

        self.horizontalLayout_25.addWidget(self.bad_unit_label)


        self.verticalLayout_11.addWidget(self.widget_67)


        self.gridLayout_7.addWidget(self.widget_65, 0, 1, 1, 1)

        self.widget_62 = QWidget(self.widget_20)
        self.widget_62.setObjectName(u"widget_62")
        self.widget_62.setMinimumSize(QSize(0, 0))
        self.widget_62.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_14 = QVBoxLayout(self.widget_62)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.widget_63 = QWidget(self.widget_62)
        self.widget_63.setObjectName(u"widget_63")
        self.widget_63.setMinimumSize(QSize(0, 0))
        self.widget_63.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_31 = QHBoxLayout(self.widget_63)
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(-1, 0, 0, 0)
        self.label_78 = QLabel(self.widget_63)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setMinimumSize(QSize(88, 30))
        self.label_78.setMaximumSize(QSize(88, 30))
        self.label_78.setFont(font4)

        self.horizontalLayout_31.addWidget(self.label_78)

        self.magazine_from = QLineEdit(self.widget_63)
        self.magazine_from.setObjectName(u"magazine_from")
        self.magazine_from.setMinimumSize(QSize(302, 30))
        self.magazine_from.setMaximumSize(QSize(302, 30))
        self.magazine_from.setFont(font2)

        self.horizontalLayout_31.addWidget(self.magazine_from)


        self.verticalLayout_14.addWidget(self.widget_63)

        self.widget_64 = QWidget(self.widget_62)
        self.widget_64.setObjectName(u"widget_64")
        self.widget_64.setMinimumSize(QSize(0, 0))
        self.widget_64.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_32 = QHBoxLayout(self.widget_64)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(9, 0, 0, 0)
        self.label_79 = QLabel(self.widget_64)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setMinimumSize(QSize(100, 30))
        self.label_79.setMaximumSize(QSize(100, 30))
        self.label_79.setFont(font4)

        self.horizontalLayout_32.addWidget(self.label_79)

        self.good_unit_label = QLabel(self.widget_64)
        self.good_unit_label.setObjectName(u"good_unit_label")
        self.good_unit_label.setMinimumSize(QSize(290, 30))
        self.good_unit_label.setMaximumSize(QSize(290, 30))
        self.good_unit_label.setFont(font2)
        self.good_unit_label.setMargin(-1)
        self.good_unit_label.setIndent(-3)

        self.horizontalLayout_32.addWidget(self.good_unit_label)


        self.verticalLayout_14.addWidget(self.widget_64)


        self.gridLayout_7.addWidget(self.widget_62, 0, 0, 1, 1)

        self.widget_61 = QWidget(self.widget_20)
        self.widget_61.setObjectName(u"widget_61")
        self.widget_61.setMinimumSize(QSize(0, 0))
        self.widget_61.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_19 = QHBoxLayout(self.widget_61)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, 0, 0, 0)
        self.label_77 = QLabel(self.widget_61)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setMinimumSize(QSize(80, 30))
        self.label_77.setMaximumSize(QSize(80, 30))
        self.label_77.setFont(font4)

        self.horizontalLayout_19.addWidget(self.label_77)

        self.operator_lineEdit = QLineEdit(self.widget_61)
        self.operator_lineEdit.setObjectName(u"operator_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.operator_lineEdit.sizePolicy().hasHeightForWidth())
        self.operator_lineEdit.setSizePolicy(sizePolicy1)
        self.operator_lineEdit.setMinimumSize(QSize(714, 30))
        self.operator_lineEdit.setMaximumSize(QSize(714, 30))
        self.operator_lineEdit.setFont(font2)

        self.horizontalLayout_19.addWidget(self.operator_lineEdit)


        self.gridLayout_7.addWidget(self.widget_61, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.widget_20)


        self.gridLayout_2.addWidget(self.strip, 2, 0, 1, 1)

        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMinimumSize(QSize(1561, 40))
        self.widget_2.setMaximumSize(QSize(1800, 40))
        self.widget_2.setStyleSheet(u"background-color: #27296c;")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        font5 = QFont()
        font5.setFamilies([u"Poppins"])
        font5.setBold(True)
        font5.setItalic(False)
        self.label_5.setFont(font5)
        self.label_5.setStyleSheet(u"color: white;")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font5)
        self.label_7.setStyleSheet(u"color: white;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_7)


        self.gridLayout_2.addWidget(self.widget_2, 3, 0, 1, 2)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.live_camera.setText("")
        self.image_1.setText("")
        self.image_1_description.setText("")
        self.image_3.setText("")
        self.image_3_description.setText("")
        self.image_5.setText("")
        self.image_5_description.setText("")
        self.image_7.setText("")
        self.image_7_description.setText("")
        self.image_9.setText("")
        self.image_9_description.setText("")
        self.image_2.setText("")
        self.image_2_description.setText("")
        self.image_4.setText("")
        self.image_4_description.setText("")
        self.image_6.setText("")
        self.image_6_description.setText("")
        self.image_8.setText("")
        self.image_8_description.setText("")
        self.image_10.setText("")
        self.image_10_description.setText("")
        self.action_button.setText("")
        self.wire_combo.setItemText(0, "")
        self.wire_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.wire_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.wire_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.wire_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.wire_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.wire_combo.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.wire_combo.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))
        self.wire_combo.setItemText(8, QCoreApplication.translate("MainWindow", u"8", None))
        self.wire_combo.setItemText(9, QCoreApplication.translate("MainWindow", u"9", None))
        self.wire_combo.setItemText(10, QCoreApplication.translate("MainWindow", u"10", None))

        self.wire_combo.setCurrentText("")
        self.export_button.setText("")
        self.current_qlabel.setText(QCoreApplication.translate("MainWindow", u" Current Strip Status", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Mag to:", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"Bad Units:", None))
        self.bad_unit_label.setText("")
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"Mag From:", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Good Units:", None))
        self.good_unit_label.setText("")
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"Operator:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"   Developed by FJMM for Fastech Synergy Philippines, Inc.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u00a9 2025   ", None))
    # retranslateUi

