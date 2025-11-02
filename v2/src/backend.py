import sys
import cv2
import numpy as np
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from frontend import Ui_MainWindow
from splashscreen import Ui_MainWindow as SplashScreenUI
from PySide6.QtOpenGLWidgets import *
from OpenGL.GL import *
from camera_module import CameraThread
from db import CaptureDB
import sqlite3
import xlsxwriter
from ultralytics import YOLO
import torch

class SaveWorkerSignals(QObject):
    success = Signal(int)
    error = Signal(str)


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
            magazine_id = db.save_capture_set(self.operator, self.mag_from, self.mag_to, self.images_and_descriptions)
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.success.emit(magazine_id)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("IVIS")

        # Initialize DB once
        db = CaptureDB()
        db.init_db()

        # Load YOLO model from local script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "best.pt")
        self.model = YOLO(model_path)
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        # Window settings persistence
        self.settings = QSettings("IVIS", "WireDetectionThesis")
        self.read_settings()

        self.cam_thread = CameraThread(camera_index=1, fps=25, width=1190, height=780)
        self.cam_thread.raw_frame_ready.connect(self.on_frame)
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

        # Keep session-persistent operator and magazine values
        self.session_operator = self.ui.operator_lineEdit.text()
        self.session_magazine_from = self.ui.magazine_from.text()
        self.session_magazine_to = self.ui.magazine_to.text()

        # Initialize magazine capture count and limit attributes
        self.magazine_capture_count = 0
        self.magazine_capture_limit = 20

    # Converts QImage to numpy ndarray in RGB format
    def qimage_to_ndarray(self, qimg):
        qimg = qimg.convertToFormat(QImage.Format.Format_RGB888)
        width = qimg.width()
        height = qimg.height()
        ptr = qimg.constBits()
        ptr = memoryview(ptr).cast('B')
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, 3))
        return arr


    # Annotate frame with detection boxes and labels
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

    # Method to run inference on incoming camera frames and display annotated results
    def on_frame(self, frame):
        # frame = self.qimage_to_ndarray(qimg)
        if frame is None:
            return

        # -- Convert input to BGR for model (Ultralytics expects BGR) --
        # If your qimage_to_ndarray already returns BGR, skip this conversion.
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # NOTE: consider running `self.model` in a worker thread instead of GUI thread.
        try:
            results = self.model(bgr_frame)[0]
        except Exception as e:
            # If inference fails, fall back to showing original frame
            print("Inference error:", e)
            display_rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        else:
            # Try to get annotated image from results.plot()
            try:
                annotated = results.plot()
            except Exception as e:
                print("Plot error:", e)
                annotated = None

            if isinstance(annotated, np.ndarray):
                # Ensure contiguous memory
                annotated = np.ascontiguousarray(annotated)

                # If float in [0,1] scale to 0..255
                if np.issubdtype(annotated.dtype, np.floating):
                    annotated = np.clip(annotated * 255.0, 0, 255).astype(np.uint8)
                elif annotated.dtype != np.uint8:
                    annotated = annotated.astype(np.uint8)

                # Handle channel counts: prefer 3-channel BGR -> convert to RGB
                if annotated.ndim == 3 and annotated.shape[2] == 3:
                    # Most plotting functions produce BGR; convert to RGB for QImage
                    display_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                elif annotated.ndim == 2:
                    # grayscale -> to RGB
                    display_rgb = cv2.cvtColor(annotated, cv2.COLOR_GRAY2RGB)
                elif annotated.ndim == 3 and annotated.shape[2] == 4:
                    # BGRA -> convert to RGBA then to RGB (drop alpha)
                    rgba = cv2.cvtColor(annotated, cv2.COLOR_BGRA2RGBA)
                    display_rgb = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
                else:
                    # unexpected format -> fallback to original frame
                    display_rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            else:
                # No annotated array -> show original frame
                display_rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

        # Ensure contiguous and uint8
        display_rgb = np.ascontiguousarray(display_rgb)
        if display_rgb.dtype != np.uint8:
            display_rgb = np.clip(display_rgb, 0, 255).astype(np.uint8)

        h, w = display_rgb.shape[:2]
        ch = 3  # we guarantee RGB 3 channels above
        bytes_per_line = ch * w

        # Create QImage from numpy buffer. Use .copy() to avoid lifetime issues if necessary.
        qimage = QImage(display_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
        pix = QPixmap.fromImage(qimage)

        target_w = self.ui.live_camera.width()
        target_h = self.ui.live_camera.height()
        scaled = pix.scaled(target_w, target_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.live_camera.setPixmap(scaled)


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
        self.ui.operator_lineEdit.setEnabled(False)
        self.ui.magazine_from.setEnabled(False)
        self.ui.magazine_to.setEnabled(False)
        self.ui.export_button.setEnabled(False)
        QTimer.singleShot(150, lambda: self.ui.action_button.setEnabled(True))
        if self.is_capturing:
            self.stop_capture()
            self.is_capturing = False
        else:
            self.is_capturing = True
            self.start_auto_capture()

    def start_auto_capture(self):
        if not self.is_capturing:
            # Don't start capture if flagged stopped
            return
        if self.magazine_capture_count >= self.magazine_capture_limit:
            QMessageBox.information(self, "Capture Limit Reached",
                                    f"Maximum automatic magazine captures ({self.magazine_capture_limit}) reached.")
            return
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
        if self.wait_timer.isActive():
            self.wait_timer.stop()

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

    def on_save_success(self, magazine_id):
        print(f"Capture saved with magazine id: {magazine_id}")
        self.magazine_capture_count += 1
        if self.magazine_capture_count >= self.magazine_capture_limit:
            self.capture_timer.stop()
            self.wait_timer.stop()
            QMessageBox.information(self, "Capture Limit Reached",
                                    f"Reached maximum automatic magazine captures ({self.magazine_capture_limit}). Stopping further captures.")
            self.is_capturing = False
            self.ui.action_button.setEnabled(True)
            self.ui.operator_lineEdit.setEnabled(True)
            self.ui.magazine_from.setEnabled(True)
            self.ui.magazine_to.setEnabled(True)
            self.ui.export_button.setEnabled(True)

        self.reset_images()
        self.captured_count = 0

    def on_save_error(self, error_msg):
        QMessageBox.warning(self, "Save Error", f"Failed to save capture set:\n{error_msg}")

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
            db = CaptureDB()
            all_data = []
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, operator, magazine_from, magazine_to, created_at FROM magazines")
            magazines = cursor.fetchall()

            for mag in magazines:
                mag_id, operator, mag_from, mag_to, created_at = mag
                cursor.execute("SELECT id, package_number FROM packages WHERE magazine_id = ?", (mag_id,))
                packages = cursor.fetchall()
                for pkg_id, pkg_num in packages:
                    cursor.execute(
                        "SELECT stripe_number, file_path, description, saved_at FROM stripes WHERE package_id = ? ORDER BY stripe_number ASC",
                        (pkg_id,)
                    )
                    stripes = cursor.fetchall()
                    for stripe in stripes:
                        stripe_num, file_path, description, saved_at = stripe
                        all_data.append([
                            mag_id,
                            operator,
                            mag_from,
                            mag_to,
                            created_at,
                            pkg_num,
                            stripe_num,
                            os.path.basename(file_path),
                            file_path,
                            description,
                            saved_at,
                        ])

            conn.close()

            headers = [
                "Magazine ID",
                "Operator",
                "Magazine From",
                "Magazine To",
                "Magazine Created At",
                "Package Number",
                "Stripe Number",
                "Image File",
                "Image Path",
                "Description",
                "Image Saved At"
            ]

            if export_type == "csv":
                import csv
                with open(save_path, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header excluding "Image Path"
                    writer.writerow([h for h in headers if h != "Image Path"])
                    for row in all_data:
                        # Exclude Image Path (index 8)
                        row_out = row[:8] + row[9:]
                        writer.writerow(row_out)

            else:
                workbook = xlsxwriter.Workbook(save_path)
                worksheet = workbook.add_worksheet('Export')

                # Define column widths explicitly (excluding Image Path which is hidden)
                col_widths = {
                    0: 10,   # Magazine ID
                    1: 40,   # Operator
                    2: 20,   # Magazine From
                    3: 20,   # Magazine To
                    4: 25,   # Magazine Created At
                    5: 12,   # Package Number
                    6: 12,   # Stripe Number
                    7: 25,   # Image File
                    8: 40,   # Image Path (hidden)
                    9: 40,   # Description
                    10: 40   # Image Saved At
                }

                # Write header row (excluding "Image Path")
                col = 0
                for i, header in enumerate(headers):
                    if header != "Image Path":
                        worksheet.write(0, col, header)
                        worksheet.set_column(col, col, col_widths[i])
                        col += 1

                # Write data rows excluding Image Path (index 8)
                for row_idx, row in enumerate(all_data, start=1):
                    col = 0
                    for i, cell_value in enumerate(row):
                        if i != 8:  # Skip Image Path
                            worksheet.write(row_idx, col, cell_value)
                            col += 1

                    # Set row height for image rows
                    worksheet.set_row(row_idx, 90)

                    # Insert image if file exists (scaled)
                    img_path = row[8]
                    if os.path.isfile(img_path):
                        img = cv2.imread(img_path)
                        if img is not None:
                            h, w = img.shape[:2]
                            cell_width_pixels = 270 * 7
                            cell_height_pixels = 90
                            x_scale = min(1, cell_width_pixels / w)
                            y_scale = min(1, cell_height_pixels / h)
                            scale = min(x_scale, y_scale)
                            # Image File column index is 7, but excludes Image Path => index 7 in sheet
                            worksheet.insert_image(row_idx, 7, img_path, {'x_scale': scale, 'y_scale': scale, 'object_position': 1})

                workbook.close()

            QMessageBox.information(self, "Export Successful", f"Data exported successfully to:\n{save_path}")

        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Failed to export data:\n{str(e)}")

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
