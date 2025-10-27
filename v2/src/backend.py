import sys
import cv2
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from frontend import Ui_MainWindow
from splashscreen import Ui_MainWindow as SplashScreenUI
from PySide6.QtOpenGLWidgets import *
from OpenGL.GL import *
from camera_module import CameraThread
from db import CaptureDB
import pandas as pd
import os
import sqlite3
import shutil
from datetime import *
import xlsxwriter

class SaveWorkerSignals(QObject):
    success = Signal(int)  # emits capture_id on success
    error = Signal(str)    # emits error message on failure


class SaveCaptureWorker(QRunnable):
    def __init__(self, operator, mag_from, mag_to, images_and_descriptions):
        super().__init__()
        self.operator = operator
        self.mag_from = mag_from
        self.mag_to = mag_to
        self.images_and_descriptions = images_and_descriptions
        self.signals = SaveWorkerSignals()

    def run(self):
        try:
            db = CaptureDB()
            capture_id = db.save_capture_set(self.operator, self.mag_from, self.mag_to, self.images_and_descriptions)
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.success.emit(capture_id)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("IVIS")

        # Initialize DB once
        db = CaptureDB()
        db.init_db()

        # Window settings persistence
        self.settings = QSettings("IVIS", "WireDetectionThesis")
        self.read_settings()

        self.cam_thread = CameraThread(camera_index=0, fps=25, width=1190, height=780)
        self.cam_thread.frame_ready.connect(self.on_frame)
        self.cam_thread.start()

        self.captured_images = []
        self.captured_count = 0
        self.ui.wire_combo.view().setRowHidden(0, True)

        self.capture_timer = QTimer()
        self.capture_timer.setInterval(500)
        self.capture_timer.timeout.connect(self.capture_image)

        self.wait_timer = QTimer()
        self.wait_timer.setSingleShot(True)
        self.wait_timer.timeout.connect(self.start_capture_cycle)

        self.is_paused = False
        self.is_recording = False
        self.is_capturing = False

        self.ui.action_button.clicked.connect(self.toggle_capture)
        self.ui.magazine_from.textChanged.connect(self.get_magazine_from)
        self.ui.magazine_to.textChanged.connect(self.get_magazine_to)
        self.ui.operator_lineEdit.textChanged.connect(self.get_operator_name)
        self.ui.export_button.clicked.connect(self.on_export_button_clicked)
        self.ui.wire_combo.currentTextChanged.connect(self.get_wire)

        self.current_detections = None

        self.thread_pool = QThreadPool.globalInstance()

        # Keep session-persistent operator value
        self.session_operator = self.ui.operator_lineEdit.text()
        # Keep track of magazines
        self.session_magazine_from = self.ui.magazine_from.text()
        self.session_magazine_to = self.ui.magazine_to.text()

    # Window persistence
    def read_settings(self):
        pos = self.settings.value("pos", None)
        size = self.settings.value("size", None)
        if pos is not None and size is not None:
            self.move(pos)
            self.resize(size)
        if self.settings.value("maximized", False, type=bool):
            self.showMaximized()

    def write_settings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())
        self.settings.setValue("maximized", self.isMaximized())

    def closeEvent(self, event):
        self.write_settings()
        if hasattr(self, 'cam_thread') and self.cam_thread.isRunning():
            self.cam_thread.stop()
        super().closeEvent(event)
        event.accept()

    def toggle_capture(self):
        self.ui.action_button.setEnabled(False)
        QTimer.singleShot(150, lambda: self.ui.action_button.setEnabled(True))
        if self.is_capturing:
            self.stop_capture()
            self.is_capturing = False
        else:
            self.start_auto_capture()
            self.is_capturing = True

    def start_auto_capture(self):
        if self.is_paused:
            self.capture_timer.start()
            self.is_paused = False
        else:
            self.captured_count = 0
            self.captured_images = []
            self.reset_images()
            self.capture_timer.start()

    def stop_capture(self):
        if self.capture_timer.isActive():
            self.capture_timer.stop()
            self.is_paused = True

    def capture_image(self):
        if self.captured_count >= 10:
            self.capture_timer.stop()
            self.save_current_capture_set()
            self.wait_timer.start(3000)
            return

        frame = getattr(self.cam_thread, 'latest_frame', None)
        if frame is None:
            print("No camera frame yet.")
            return

        # Store raw full-size frame for export
        raw_frame = frame.copy()

        # Resize for GUI display
        resized_frame = cv2.resize(frame, (150, 150))

        # Convert to RGB for Qt image display
        rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Set pixmap to QLabel
        label_name = f"image_{self.captured_count + 1}"
        label = getattr(self.ui, label_name, None)
        if label is not None:
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.repaint()
        else:
            print(f"Label {label_name} not found.")

        # Append raw frame for export/storage instead of resized
        self.captured_images.append(raw_frame)
        self.captured_count += 1


    def reset_images(self):
        for i in range(1, 11):
            label = getattr(self.ui, f"image_{i}", None)
            if label:
                label.clear()
        self.captured_images = []
        self.captured_count = 0

    def save_current_capture_set(self):
        operator = self.ui.operator_lineEdit.text() or self.session_operator
        magazine_from = self.ui.magazine_from.text() or self.session_magazine_from
        magazine_to = self.ui.magazine_to.text() or self.session_magazine_to
        self.session_operator = operator  # persist in session
        self.session_magazine_from = magazine_from
        self.session_magazine_to = magazine_to

        images_and_descriptions = []
        for idx in range(len(self.captured_images)):
            _, jpeg_bytes = cv2.imencode(".jpg", self.captured_images[idx])
            desc_widget = getattr(self.ui, f"image_{idx+1}_description", None)
            desc = desc_widget.text() if desc_widget else ""
            images_and_descriptions.append((jpeg_bytes.tobytes(), desc))

        worker = SaveCaptureWorker(operator, magazine_from, magazine_to, images_and_descriptions)
        worker.signals.success.connect(self.on_save_success)
        worker.signals.error.connect(self.on_save_error)
        self.thread_pool.start(worker)

    def on_save_success(self, capture_id):
        print(f"Capture saved with id: {capture_id}")
        # Reset images and UI after saving
        self.reset_images()
        self.captured_count = 0
        
    def on_save_error(self, error_msg):
        QMessageBox.warning(self, "Save Error", f"Failed to save capture set:\n{error_msg}")
        # Do not reset magazines or operator; keep UI consistent

    def get_wire(self, selected_text):
        if selected_text == "NO. OF WIRE/S":
            return None
        try:
            return int(selected_text)
        except ValueError:
            return None

    def get_magazine_from(self, text):
        return text

    def get_magazine_to(self, text):
        return text

    def get_operator_name(self, text):
        return text

    def get_bad_units(self):
        return self.ui.bad_unit_label.text()

    def get_good_units(self):
        return self.ui.good_unit_label.text()

    def annotate_frame(self, frame):
        detections = getattr(self, 'current_detections', None)
        out = frame.copy()
        if not detections:
            return out
        for det in detections:
            x, y, w, h = det['box']
            cls = det.get('class', 'obj')
            score = det.get('score', None)
            color = (0, 255, 0)
            cv2.rectangle(out, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
            label = cls
            if score is not None:
                label = f"{cls}: {score:.2f}"
            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(out, (int(x), int(y) - text_h - 8), (int(x) + text_w, int(y)), color, -1)
            cv2.putText(out, label, (int(x), int(y) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        return out
    
    def on_export_button_clicked(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Select Export File Type")
        msg_box.setText("Choose the file type for export:")
        csv_button = msg_box.addButton("CSV", QMessageBox.ActionRole)
        excel_button = msg_box.addButton("Excel", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        msg_box.exec()

        if msg_box.clickedButton() == cancel_button:
            return

        if msg_box.clickedButton() == csv_button:
            file_filter = "CSV files (*.csv)"
            default_ext = ".csv"
            export_type = "csv"
        elif msg_box.clickedButton() == excel_button:
            file_filter = "Excel files (*.xlsx *.xls)"
            default_ext = ".xlsx"
            export_type = "excel"
        else:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Exported File", "", file_filter)
        if not save_path:
            return

        if not save_path.lower().endswith(default_ext):
            save_path += default_ext

        try:
            import cv2
            import xlsxwriter
            db = CaptureDB()
            all_data = []
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, operator, magazine_from, magazine_to, created_at FROM capture_set")
            capture_sets = cursor.fetchall()

            for cap in capture_sets:
                cap_id, operator, mag_from, mag_to, created_at = cap
                cursor.execute("SELECT image_index, file_path, description, saved_at FROM capture_image WHERE capture_set_id=?", (cap_id,))
                images = cursor.fetchall()

                for img in images:
                    image_index, file_path, description, saved_at = img
                    all_data.append([
                        cap_id,
                        operator,
                        mag_from,
                        mag_to,
                        created_at,
                        image_index,
                        os.path.basename(file_path),
                        file_path,
                        description,
                        saved_at
                    ])

            conn.close()

            headers = [
                "Capture ID",
                "Operator",
                "Magazine From",
                "Magazine To",
                "Capture Created At",
                "Image Index",
                "Image File",
                "Image Path",
                "Description",
                "Image Saved At"
            ]

            if export_type == "csv":
                import csv
                with open(save_path, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header excluding Image Path
                    writer.writerow([h for h in headers if h != "Image Path"])
                    for row in all_data:
                        # Exclude Image Path (index 7)
                        row_out = row[:7] + row[8:]
                        writer.writerow(row_out)

            else:
                workbook = xlsxwriter.Workbook(save_path)
                worksheet = workbook.add_worksheet('Export')

                # Define column widths explicitly (excluding Image Path which is hidden)
                col_widths = {
                    0: 10,  # Capture ID
                    1: 40,  # Operator
                    2: 20,  # Magazine From
                    3: 20,  # Magazine To
                    4: 25,  # Capture Created At
                    5: 11,  # Image Index
                    6: 25,  # Image File
                    7: 40, #Image Path - will be hidden
                    8: 40,  # Description
                    9: 40   # Image Saved At
                }

                # Write header row (excluding "Image Path")
                col = 0
                for i, header in enumerate(headers):
                    if header != "Image Path":
                        worksheet.write(0, col, header)
                        worksheet.set_column(col, col, col_widths[i])
                        col += 1


                # Write data rows excluding Image Path (index 7)
                for row_idx, row in enumerate(all_data, start=1):
                    col = 0
                    for i, cell_value in enumerate(row):
                        if i != 7:  # Skip Image Path
                            worksheet.write(row_idx, col, cell_value)
                            col += 1

                    # Set row height for image rows if needed
                    worksheet.set_row(row_idx, 90)

                    # Insert image if file exists (scaled)
                    img_path = row[7]
                    if os.path.isfile(img_path):
                        img = cv2.imread(img_path)
                        if img is not None:
                            h, w = img.shape[:2]
                            cell_width_pixels = 270 * 7
                            cell_height_pixels = 90
                            x_scale = min(1, cell_width_pixels / w)
                            y_scale = min(1, cell_height_pixels / h)
                            scale = min(x_scale, y_scale)
                            # Image File column index is 6, but column in sheet excludes Image Path => 6 in sheet
                            worksheet.insert_image(row_idx, 6, img_path, {'x_scale': scale, 'y_scale': scale, 'object_position': 1})

                workbook.close()

            QMessageBox.information(self, "Export Successful", f"Data exported successfully to:\n{save_path}")
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Failed to export data:\n{str(e)}")


    def on_frame(self, qimg):
        pix = QPixmap.fromImage(qimg)
        target_w = self.ui.live_camera.width()
        target_h = self.ui.live_camera.height()
        scaled = pix.scaled(target_w, target_h, Qt.KeepAspectRatio)
        self.ui.live_camera.setPixmap(scaled)

    def start_capture_cycle(self):
        self.captured_count = 0
        self.captured_images = []
        self.reset_images()
        self.capture_timer.start()


class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
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
    window = SplashScreen()
    sys.exit(app.exec())
