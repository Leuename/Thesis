import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from frontend import Ui_MainWindow
from splashscreen import Ui_MainWindow as SplashScreenUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("IVIS")
        self.ui.magazine_from.textChanged.connect(self.get_magazine_from)
        self.ui.magazine_to.textChanged.connect(self.get_magazine_to)
        self.ui.operator_lineEdit.textChanged.connect(self.get_operator_name)

        # Connect signal correctly and access wire_combo from ui
        self.ui.export_button.clicked.connect(self.on_export_button_clicked)
        self.ui.wire_combo.currentTextChanged.connect(self.get_wire)

    def get_wire(self, selected_text):
        if selected_text == "NO. OF WIRE/S":
            return None
        try:
            wire_number = int(selected_text)
            return wire_number
        except ValueError:
            return None
    
    def get_magazine_from(self, from_magazine_text):
        from_magazine_text = self.ui.magazine_from.text()
        return from_magazine_text
        
    def get_magazine_to(self, to_magazine_text):
        to_magazine_text = self.ui.magazine_to.text()
        return to_magazine_text

    def get_operator_name(self, operator_name):
        operator_name = self.ui.operator_lineEdit.text()
        return operator_name
        
    def get_bad_units(self, bad_text):
        # Placeholder for future implementation
        bad_text = self.ui.bad_unit_label.text()
        return bad_text
    
    def get_good_units(self, good_text):
        # Placeholder for future implementation
        good_text = self.ui.bad_unit_label.text()
        return good_text
    


    def stop_button(self):
        if self.ui.stop_button.isChecked():
            self.ui.stop_button.setText("STOP!")
            
    def start_button(self):
        if self.ui.start_button.isChecked():
            self.ui.start_button.setText("START!")
    
    def on_export_button_clicked(self):
        # Step 1: Ask user to select file type with a message box
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Select Export File Type")
        msg_box.setText("Choose the file type for export:")
        csv_button = msg_box.addButton("CSV", QMessageBox.ActionRole)
        excel_button = msg_box.addButton("Excel", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        msg_box.exec()

        if msg_box.clickedButton() == cancel_button:
            return  # User cancelled export

        # Determine selected file type and extension
        if msg_box.clickedButton() == csv_button:
            file_filter = "CSV files (*.csv)"
            default_ext = ".csv"
        elif msg_box.clickedButton() == excel_button:
            file_filter = "Excel files (*.xlsx *.xls)"
            default_ext = ".xlsx"
        else:
            return

        # Step 2: Open file save dialog with the selected filter
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Exported File",
            "",
            file_filter
        )

        if save_path:
            # Optionally enforce file extension if not provided
            if not save_path.lower().endswith(default_ext):
                save_path += default_ext

            print(f"User selected file path: {save_path}")
            # Proceed to save your data to save_path here
    
    def image_display_1(self):
        # Placeholder for future implementatio
        pass
    def image_display_2(self):
        # Placeholder for future implementation
        pass
    def image_display_3(self):
        # Placeholder for future implementation
        pass
    def image_display_4(self):
        # Placeholder for future implementation
        pass
    def image_display_5(self):
        # Placeholder for future implementation
        pass
    def image_display_6(self):
        # Placeholder for future implementation
        pass
    def image_display_7(self):
        # Placeholder for future implementation
        pass
    def image_display_8(self):
        # Placeholder for future implementation
        pass
    def image_display_9(self):
        # Placeholder for future implementation
        pass
    def image_display_10(self):
        # Placeholder for future implementation
        pass
    


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = SplashScreenUI()
        self.ui.setupUi(self)
        QTimer.singleShot(2500, self.openMainWindow)
        self.show()

    def openMainWindow(self):
        self.main_win = MainWindow()
        self.main_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Instantiate your SplashScreen class, not the UI definition
    window = SplashScreen()
    sys.exit(app.exec())
