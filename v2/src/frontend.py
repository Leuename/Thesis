
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import *
import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QSize(1920, 1080))
        MainWindow.setMaximumSize(QSize(1920, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-10, 0, 1920, 1080))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(1920, 1080))
        self.frame.setMaximumSize(QSize(1920, 1080))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(10, 1030, 1910, 40))
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(1910, 40))
        self.widget_2.setMaximumSize(QSize(1910, 40))
        self.widget_2.setStyleSheet(u"background-color: #27296c;")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setFamilies([u"Poppins"])
        font.setBold(True)
        font.setItalic(False)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"color: white;")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.horizontalSpacer = QSpacerItem(1690, 19, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(u"color: white;")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(10, 0, 1191, 1021))
        self.frame_4.setMinimumSize(QSize(930, 0))
        self.frame_4.setMaximumSize(QSize(353533, 5383838))
        self.frame_4.setStyleSheet(u"#frame_4{\n"
"	border:none;\n"
"}")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.display = QOpenGLWidget(self.frame_4)
        self.display.setObjectName(u"display")
        self.display.setGeometry(QRect(10, 10, 1191, 811))
        self.display.setMinimumSize(QSize(1190, 780))
        self.display.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 790, 1191, 271))
        self.frame_3.setMinimumSize(QSize(900, 220))
        self.frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3.setStyleSheet(u"#frame_3{\n"
"\n"
"	border:none;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.widget_14 = QWidget(self.frame_3)
        self.widget_14.setObjectName(u"widget_14")
        self.horizontalLayout_16 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.current_frame_2 = QFrame(self.widget_14)
        self.current_frame_2.setObjectName(u"current_frame_2")
        self.current_frame_2.setMinimumSize(QSize(820, 170))
        self.current_frame_2.setMaximumSize(QSize(820, 170))
        self.current_frame_2.setStyleSheet(u"#current_frame_2{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"    border-top: none;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.current_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.current_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.current_label_2 = QLabel(self.current_frame_2)
        self.current_label_2.setObjectName(u"current_label_2")
        self.current_label_2.setGeometry(QRect(2, 0, 820, 39))
        self.current_label_2.setMinimumSize(QSize(805, 0))
        self.current_label_2.setMaximumSize(QSize(16777215, 45))
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.current_label_2.setFont(font1)
        self.current_label_2.setStyleSheet(u"#current_label_2 {\n"
"        background-color: #27296c;   /* dark blue header */\n"
"        color: white;\n"
"        font-weight: bold;\n"
"        font-size: 14pt;\n"
"        padding: 6px 10px;\n"
"        border: none;\n"
"        border-bottom: none;         /* so it merges with frame */\n"
"        border-top-left-radius: 1px;\n"
"        border-top-right-radius: 1px;\n"
"		border-radius:50px;\n"
"}\n"
"\n"
"")
        self.current_label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.widget_18 = QWidget(self.current_frame_2)
        self.widget_18.setObjectName(u"widget_18")
        self.widget_18.setGeometry(QRect(-8, 53, 791, 105))
        self.widget_18.setMinimumSize(QSize(0, 0))
        self.widget_18.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_5 = QGridLayout(self.widget_18)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.widget_53 = QWidget(self.widget_18)
        self.widget_53.setObjectName(u"widget_53")
        self.widget_53.setMinimumSize(QSize(0, 0))
        self.widget_53.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_17 = QHBoxLayout(self.widget_53)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, 0, 0, 0)
        self.label_73 = QLabel(self.widget_53)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setMinimumSize(QSize(0, 0))
        self.label_73.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Poppins"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_73.setFont(font2)

        self.horizontalLayout_17.addWidget(self.label_73)

        self.operator_lineEdit = QLineEdit(self.widget_53)
        self.operator_lineEdit.setObjectName(u"operator_lineEdit")
        self.operator_lineEdit.setMinimumSize(QSize(0, 0))
        self.operator_lineEdit.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setPointSize(12)
        self.operator_lineEdit.setFont(font3)

        self.horizontalLayout_17.addWidget(self.operator_lineEdit)


        self.gridLayout_5.addWidget(self.widget_53, 1, 0, 1, 2)

        self.widget_50 = QWidget(self.widget_18)
        self.widget_50.setObjectName(u"widget_50")
        self.widget_50.setMinimumSize(QSize(0, 0))
        self.widget_50.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_11 = QVBoxLayout(self.widget_50)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.widget_51 = QWidget(self.widget_50)
        self.widget_51.setObjectName(u"widget_51")
        self.widget_51.setMinimumSize(QSize(0, 0))
        self.widget_51.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_27 = QHBoxLayout(self.widget_51)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, 0, 0)
        self.label_71 = QLabel(self.widget_51)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setMinimumSize(QSize(0, 0))
        self.label_71.setMaximumSize(QSize(16777215, 16777215))
        self.label_71.setFont(font2)

        self.horizontalLayout_27.addWidget(self.label_71)

        self.magazine_from = QLineEdit(self.widget_51)
        self.magazine_from.setObjectName(u"magazine_from")
        self.magazine_from.setMinimumSize(QSize(0, 0))
        self.magazine_from.setMaximumSize(QSize(16777215, 16777215))
        self.magazine_from.setFont(font3)

        self.horizontalLayout_27.addWidget(self.magazine_from)


        self.verticalLayout_11.addWidget(self.widget_51)

        self.widget_52 = QWidget(self.widget_50)
        self.widget_52.setObjectName(u"widget_52")
        self.widget_52.setMinimumSize(QSize(0, 0))
        self.widget_52.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_28 = QHBoxLayout(self.widget_52)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(9, 0, 0, 0)
        self.label_72 = QLabel(self.widget_52)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setMinimumSize(QSize(100, 0))
        self.label_72.setMaximumSize(QSize(100, 16777215))
        self.label_72.setFont(font2)

        self.horizontalLayout_28.addWidget(self.label_72)

        self.good_unit_label = QLabel(self.widget_52)
        self.good_unit_label.setObjectName(u"good_unit_label")
        self.good_unit_label.setMinimumSize(QSize(0, 0))
        self.good_unit_label.setMaximumSize(QSize(16777215, 16777215))
        self.good_unit_label.setFont(font3)
        self.good_unit_label.setMargin(-1)
        self.good_unit_label.setIndent(-3)

        self.horizontalLayout_28.addWidget(self.good_unit_label)


        self.verticalLayout_11.addWidget(self.widget_52)


        self.gridLayout_5.addWidget(self.widget_50, 0, 0, 1, 1)

        self.widget_47 = QWidget(self.widget_18)
        self.widget_47.setObjectName(u"widget_47")
        self.widget_47.setMinimumSize(QSize(0, 0))
        self.widget_47.setMaximumSize(QSize(16777215, 70))
        self.verticalLayout_8 = QVBoxLayout(self.widget_47)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.widget_48 = QWidget(self.widget_47)
        self.widget_48.setObjectName(u"widget_48")
        self.widget_48.setMinimumSize(QSize(0, 0))
        self.widget_48.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_20 = QHBoxLayout(self.widget_48)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, 0, 0, 0)
        self.label_67 = QLabel(self.widget_48)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setMinimumSize(QSize(0, 0))
        self.label_67.setMaximumSize(QSize(16777215, 16777215))
        self.label_67.setFont(font2)

        self.horizontalLayout_20.addWidget(self.label_67)

        self.magazine_to = QLineEdit(self.widget_48)
        self.magazine_to.setObjectName(u"magazine_to")
        self.magazine_to.setMinimumSize(QSize(0, 0))
        self.magazine_to.setMaximumSize(QSize(16777215, 16777215))
        self.magazine_to.setFont(font3)

        self.horizontalLayout_20.addWidget(self.magazine_to)


        self.verticalLayout_8.addWidget(self.widget_48)

        self.widget_49 = QWidget(self.widget_47)
        self.widget_49.setObjectName(u"widget_49")
        self.widget_49.setMinimumSize(QSize(0, 0))
        self.widget_49.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_21 = QHBoxLayout(self.widget_49)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 0, 0, 0)
        self.label_68 = QLabel(self.widget_49)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setMinimumSize(QSize(85, 0))
        self.label_68.setMaximumSize(QSize(85, 16777215))
        self.label_68.setFont(font2)

        self.horizontalLayout_21.addWidget(self.label_68)

        self.bad_unit_label = QLabel(self.widget_49)
        self.bad_unit_label.setObjectName(u"bad_unit_label")
        self.bad_unit_label.setMinimumSize(QSize(0, 0))
        self.bad_unit_label.setMaximumSize(QSize(16777215, 16777215))
        self.bad_unit_label.setFont(font3)
        self.bad_unit_label.setMargin(-1)
        self.bad_unit_label.setIndent(-3)

        self.horizontalLayout_21.addWidget(self.bad_unit_label)


        self.verticalLayout_8.addWidget(self.widget_49)


        self.gridLayout_5.addWidget(self.widget_47, 0, 1, 1, 1)


        self.horizontalLayout_16.addWidget(self.current_frame_2)


        self.horizontalLayout_15.addWidget(self.widget_14)

        self.ini_frame_2 = QFrame(self.frame_3)
        self.ini_frame_2.setObjectName(u"ini_frame_2")
        self.ini_frame_2.setMinimumSize(QSize(330, 0))
        self.ini_frame_2.setMaximumSize(QSize(330, 170))
        self.ini_frame_2.setStyleSheet(u"#ini_frame_2{\n"
"    border-left: 4px solid #27296c;\n"
"    border-right: 4px solid #27296c;\n"
"    border-bottom: 5px solid #27296c;\n"
"	border-top:5px solid #27296c;\n"
"    border-radius: 4px;\n"
"    background: white;\n"
"}\n"
"")
        self.ini_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.ini_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.ini_frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.widget_15 = QWidget(self.ini_frame_2)
        self.widget_15.setObjectName(u"widget_15")
        self.horizontalLayout_18 = QHBoxLayout(self.widget_15)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.export_button = QPushButton(self.widget_15)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setMinimumSize(QSize(0, 30))
        self.export_button.setMaximumSize(QSize(16777215, 30))
        font4 = QFont()
        font4.setFamilies([u"Poppins"])
        font4.setPointSize(20)
        self.export_button.setFont(font4)

        self.horizontalLayout_18.addWidget(self.export_button)


        self.gridLayout_6.addWidget(self.widget_15, 2, 0, 1, 1)

        self.widget_21 = QWidget(self.ini_frame_2)
        self.widget_21.setObjectName(u"widget_21")
        self.widget_21.setMinimumSize(QSize(315, 60))
        self.widget_21.setMaximumSize(QSize(315, 60))
        self.formLayout_2 = QFormLayout(self.widget_21)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.wire_combo = QComboBox(self.widget_21)
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
        self.wire_combo.addItem("")
        self.wire_combo.setObjectName(u"wire_combo")
        self.wire_combo.setMinimumSize(QSize(300, 40))
        self.wire_combo.setMaximumSize(QSize(300, 40))
        self.wire_combo.setFont(font3)
        self.wire_combo.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.wire_combo.setStyleSheet(u"border: 3px solid #27296C;\n"
"border-radius: 8px;\n"
"")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.wire_combo)


        self.gridLayout_6.addWidget(self.widget_21, 0, 0, 1, 1)

        self.widget_19 = QWidget(self.ini_frame_2)
        self.widget_19.setObjectName(u"widget_19")
        self.widget_19.setMinimumSize(QSize(315, 60))
        self.widget_19.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_19 = QHBoxLayout(self.widget_19)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.stop_button = QPushButton(self.widget_19)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setMinimumSize(QSize(150, 30))
        self.stop_button.setMaximumSize(QSize(16777215, 30))
        self.stop_button.setFont(font4)

        self.horizontalLayout_19.addWidget(self.stop_button)

        self.start_button = QPushButton(self.widget_19)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setMinimumSize(QSize(150, 30))
        self.start_button.setMaximumSize(QSize(150, 30))
        self.start_button.setFont(font4)
        self.start_button.setStyleSheet(u"color:white;\n"
"background-color: #27296c;")

        self.horizontalLayout_19.addWidget(self.start_button)


        self.gridLayout_6.addWidget(self.widget_19, 1, 0, 1, 1)


        self.horizontalLayout_15.addWidget(self.ini_frame_2)

        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(1200, 10, 730, 1020))
        self.widget.setMinimumSize(QSize(730, 1020))
        self.widget.setMaximumSize(QSize(730, 1020))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.camera_widget_1 = QWidget(self.widget)
        self.camera_widget_1.setObjectName(u"camera_widget_1")
        self.camera_widget_1.setMinimumSize(QSize(350, 1000))
        self.camera_widget_1.setMaximumSize(QSize(350, 1000))
        self.camera_widget_1.setStyleSheet(u"#cam2{\n"
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
        self.verticalLayout_10 = QVBoxLayout(self.camera_widget_1)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.cam2 = QWidget(self.camera_widget_1)
        self.cam2.setObjectName(u"cam2")
        self.horizontalLayout_52 = QHBoxLayout(self.cam2)
        self.horizontalLayout_52.setSpacing(0)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(0, -1, 0, -1)
        self.image_2 = QLabel(self.cam2)
        self.image_2.setObjectName(u"image_2")
        font5 = QFont()
        font5.setFamilies([u"Poppins"])
        self.image_2.setFont(font5)

        self.horizontalLayout_52.addWidget(self.image_2)

        self.image_2_description = QLabel(self.cam2)
        self.image_2_description.setObjectName(u"image_2_description")
        self.image_2_description.setFont(font5)

        self.horizontalLayout_52.addWidget(self.image_2_description)


        self.verticalLayout_10.addWidget(self.cam2)

        self.cam4 = QWidget(self.camera_widget_1)
        self.cam4.setObjectName(u"cam4")
        self.horizontalLayout_53 = QHBoxLayout(self.cam4)
        self.horizontalLayout_53.setSpacing(0)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.horizontalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.image_4 = QLabel(self.cam4)
        self.image_4.setObjectName(u"image_4")
        self.image_4.setFont(font5)

        self.horizontalLayout_53.addWidget(self.image_4)

        self.image_4_description = QLabel(self.cam4)
        self.image_4_description.setObjectName(u"image_4_description")
        self.image_4_description.setFont(font5)

        self.horizontalLayout_53.addWidget(self.image_4_description)


        self.verticalLayout_10.addWidget(self.cam4)

        self.cam6 = QWidget(self.camera_widget_1)
        self.cam6.setObjectName(u"cam6")
        self.horizontalLayout_54 = QHBoxLayout(self.cam6)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.horizontalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.image_6 = QLabel(self.cam6)
        self.image_6.setObjectName(u"image_6")
        self.image_6.setFont(font5)

        self.horizontalLayout_54.addWidget(self.image_6)

        self.image_6_description = QLabel(self.cam6)
        self.image_6_description.setObjectName(u"image_6_description")
        self.image_6_description.setFont(font5)

        self.horizontalLayout_54.addWidget(self.image_6_description)


        self.verticalLayout_10.addWidget(self.cam6)

        self.cam8 = QWidget(self.camera_widget_1)
        self.cam8.setObjectName(u"cam8")
        self.horizontalLayout_55 = QHBoxLayout(self.cam8)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.image_8 = QLabel(self.cam8)
        self.image_8.setObjectName(u"image_8")
        self.image_8.setFont(font5)

        self.horizontalLayout_55.addWidget(self.image_8)

        self.image_8_description = QLabel(self.cam8)
        self.image_8_description.setObjectName(u"image_8_description")
        self.image_8_description.setFont(font5)

        self.horizontalLayout_55.addWidget(self.image_8_description)


        self.verticalLayout_10.addWidget(self.cam8)

        self.cam10 = QWidget(self.camera_widget_1)
        self.cam10.setObjectName(u"cam10")
        self.cam10.setFont(font5)
        self.horizontalLayout_56 = QHBoxLayout(self.cam10)
        self.horizontalLayout_56.setSpacing(0)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.image_10 = QLabel(self.cam10)
        self.image_10.setObjectName(u"image_10")
        self.image_10.setFont(font5)

        self.horizontalLayout_56.addWidget(self.image_10)

        self.image_10_description = QLabel(self.cam10)
        self.image_10_description.setObjectName(u"image_10_description")
        self.image_10_description.setFont(font5)

        self.horizontalLayout_56.addWidget(self.image_10_description)


        self.verticalLayout_10.addWidget(self.cam10)


        self.gridLayout.addWidget(self.camera_widget_1, 0, 1, 1, 1)

        self.camera_widget_2 = QWidget(self.widget)
        self.camera_widget_2.setObjectName(u"camera_widget_2")
        self.camera_widget_2.setMinimumSize(QSize(350, 1000))
        self.camera_widget_2.setMaximumSize(QSize(350, 1000))
        self.camera_widget_2.setStyleSheet(u"#cam1{\n"
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
        self.verticalLayout_12 = QVBoxLayout(self.camera_widget_2)
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.cam1 = QWidget(self.camera_widget_2)
        self.cam1.setObjectName(u"cam1")
        self.horizontalLayout_62 = QHBoxLayout(self.cam1)
        self.horizontalLayout_62.setSpacing(0)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(0, -1, 0, -1)
        self.image_1 = QLabel(self.cam1)
        self.image_1.setObjectName(u"image_1")
        self.image_1.setFont(font5)

        self.horizontalLayout_62.addWidget(self.image_1)

        self.image_1_description = QLabel(self.cam1)
        self.image_1_description.setObjectName(u"image_1_description")
        self.image_1_description.setFont(font5)

        self.horizontalLayout_62.addWidget(self.image_1_description)


        self.verticalLayout_12.addWidget(self.cam1)

        self.cam3 = QWidget(self.camera_widget_2)
        self.cam3.setObjectName(u"cam3")
        self.horizontalLayout_63 = QHBoxLayout(self.cam3)
        self.horizontalLayout_63.setSpacing(0)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.image_3 = QLabel(self.cam3)
        self.image_3.setObjectName(u"image_3")
        self.image_3.setFont(font5)

        self.horizontalLayout_63.addWidget(self.image_3)

        self.image_3_description = QLabel(self.cam3)
        self.image_3_description.setObjectName(u"image_3_description")
        self.image_3_description.setFont(font5)

        self.horizontalLayout_63.addWidget(self.image_3_description)


        self.verticalLayout_12.addWidget(self.cam3)

        self.cam5 = QWidget(self.camera_widget_2)
        self.cam5.setObjectName(u"cam5")
        self.horizontalLayout_64 = QHBoxLayout(self.cam5)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.image_5 = QLabel(self.cam5)
        self.image_5.setObjectName(u"image_5")
        self.image_5.setFont(font5)

        self.horizontalLayout_64.addWidget(self.image_5)

        self.image_5_description = QLabel(self.cam5)
        self.image_5_description.setObjectName(u"image_5_description")
        self.image_5_description.setFont(font5)

        self.horizontalLayout_64.addWidget(self.image_5_description)


        self.verticalLayout_12.addWidget(self.cam5)

        self.cam7 = QWidget(self.camera_widget_2)
        self.cam7.setObjectName(u"cam7")
        self.horizontalLayout_65 = QHBoxLayout(self.cam7)
        self.horizontalLayout_65.setSpacing(0)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.image_7 = QLabel(self.cam7)
        self.image_7.setObjectName(u"image_7")
        self.image_7.setFont(font5)

        self.horizontalLayout_65.addWidget(self.image_7)

        self.image_7_description = QLabel(self.cam7)
        self.image_7_description.setObjectName(u"image_7_description")
        self.image_7_description.setFont(font5)

        self.horizontalLayout_65.addWidget(self.image_7_description)


        self.verticalLayout_12.addWidget(self.cam7)

        self.cam9 = QWidget(self.camera_widget_2)
        self.cam9.setObjectName(u"cam9")
        self.cam9.setFont(font5)
        self.horizontalLayout_66 = QHBoxLayout(self.cam9)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.image_9 = QLabel(self.cam9)
        self.image_9.setObjectName(u"image_9")
        self.image_9.setFont(font5)

        self.horizontalLayout_66.addWidget(self.image_9)

        self.image_9_description = QLabel(self.cam9)
        self.image_9_description.setObjectName(u"image_9_description")
        self.image_9_description.setFont(font5)

        self.horizontalLayout_66.addWidget(self.image_9_description)


        self.verticalLayout_12.addWidget(self.cam9)


        self.gridLayout.addWidget(self.camera_widget_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"  Developed by FJMM for Fastech Synergy Philippines, Inc.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u00a9 2025", None))
        self.current_label_2.setText(QCoreApplication.translate("MainWindow", u" Current Strip Status", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"  Operator:", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Mag From:", None))
        self.label_72.setText(QCoreApplication.translate("MainWindow", u"Good Units:", None))
        self.good_unit_label.setText("")
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Mag to:", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"Bad Units:", None))
        self.bad_unit_label.setText("")
        self.export_button.setText(QCoreApplication.translate("MainWindow", u"EXPORT", None))
        self.wire_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"  NO. OF WIRE/S", None))
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

        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"START", None))
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
    # retranslateUi

