from __future__ import annotations
import sys
import os
import time
import threading
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtCore
from frontend import Ui_MainWindow
from splashscreen import Ui_MainWindow as SplashScreenUI
from camera_module import CameraInferenceThread
from db import CaptureDB
from typing import *
import numpy as np
import xlsxwriter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set frameless window and translucent background
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("IVIS")

        self._reset_count = 0
        self.capture_db = CaptureDB()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "best.pt")
        self.thread = CameraInferenceThread(camera_index=0, model_path=model_path, conf_thresh=0.25)
        self.thread.frame_ready.connect(self.on_frame_ready)
        self.thread.detections_ready.connect(self.on_detections_ready)

        # --- REMOVED OBSOLETE STATE ---
        # Session info is now fetched at the moment of saving, not on init.
        # Magazine/Package state is no longer tracked here.

        self.ui.minimize.clicked.connect(self.showMinimized)
        self.ui.close.clicked.connect(self.close)
        self.ui.export_button.clicked.connect(self.on_export_button_clicked)

        self._listing_enabled = False
        self._pause_listing = False
        self._list_full = False

        self.pause_timer = QTimer(self)
        self.pause_timer.setSingleShot(True)
        self.pause_timer.timeout.connect(self.resume_listing)

        self.ui.action_button.clicked.connect(self.toggle_listing)
        self.showMaximized()

        self._inference_history = []
        self._last_inference_update = 0.0

        # --- MODIFIED: Track a single save thread ---
        self._bg_save_thread: Optional[threading.Thread] = None
        self._operation_state = 'idle'
        self._toggle_lock = threading.Lock()
        
        # This setup seems redundant with the toggle_listing connect above, 
        # but preserving original logic flow.
        self.ui.action_button.clicked.disconnect()
        self.ui.action_button.clicked.connect(self._toggle_action_button)
        
        self._reset_count = 0
        self._magazine_run_count = 0  # <--- ADD THIS LINE
        self.capture_db = CaptureDB()

    def _toggle_action_button(self):
        if self._toggle_lock.acquire(blocking=False):
            try:
                if not self.check_line_edit_changes():
                    return
                if self._operation_state == 'idle':
                    self._operation_state = 'running'
                    self._listing_enabled = True
                    self._pause_listing = False
                    self._reset_count = 0 # Reset package count for new run
                    self._magazine_run_count += 1 # <--- ADD THIS LINE
                else:
                    if self._pause_listing:
                        self._pause_listing = False
                    else:
                        self._pause_listing = True
                    self._operation_state = 'idle'
            finally:
                self._toggle_lock.release()


    def _save_stripe(self, description: str, operator: str, mag_from: str, mag_to: str):
        """
        Worker function to save a single stripe in a background thread.
        This calls the new thread-safe method in CaptureDB.
        """
        try:
            self.capture_db.add_stripe(
                description=description,
                operator=operator,
                mag_from=mag_from,
                mag_to=mag_to
            )
            # print(f"Successfully saved stripe: {description}")
        except Exception as e:
            print(f"Failed to save stripe in background: {e}")
            # You could emit a signal here to show a warning in the UI
            # self.db_error_signal.emit(str(e))

    def showEvent(self, event):
        super().showEvent(event)
        if self.ui.live_camera.pixmap() is not None:
            if not self.thread.isRunning():
                self.thread.start()
        else:
            QMessageBox.warning(self, "Camera Not Available", "No camera feed detected. Please connect a camera first.")

    def closeEvent(self, event):
        try:
            self.thread.stop()
        except Exception:
            pass
        
        # --- MODIFIED: Wait for the single save thread ---
        if self._bg_save_thread and self._bg_save_thread.is_alive():
            print("Waiting for final database save to complete...")
            self._bg_save_thread.join(timeout=2.0)
            
        # --- REMOVED: `capture_db.close()` no longer exists ---
        
        event.accept()

    def toggle_listing(self):
        if not self.check_line_edit_changes():
            return
        if not self._listing_enabled:
            self._listing_enabled = True
            self._pause_listing = False
            
            # --- ADD THIS LINE ---
            self._reset_count = 0 # Reset package count for new run
            # --- END ADD ---
            
        else:
            if self._pause_listing:
                self._pause_listing = False
            else:
                self._pause_listing = True

    def check_line_edit_changes(self):
        operator = self.ui.operator_lineEdit.text().strip()
        mag_from = self.ui.magazine_from.text().strip()
        mag_to = self.ui.magazine_to.text().strip()
        missing_fields = []
        if not operator:
            missing_fields.append("Operator")
        if not mag_from:
            missing_fields.append("Magazine From")
        if not mag_to:
            missing_fields.append("Magazine To")
        if missing_fields:
            print("Missing fields: " + ", ".join(missing_fields))
            QMessageBox.warning(
                self,
                "Missing Information",
                f"Please fill in the following field(s):\n- " + "\n- ".join(missing_fields)
            )
            return False
        return True

    def resume_listing(self):
        self._pause_listing = False
        self._list_full = False
        
        # --- ADD THIS ---
        # Clear labels now, *after* the pause is over
        label_names = ['one','two','three','four','five','six','seven','eight','nine','ten']
        for label_name in label_names:
            label = getattr(self.ui, label_name, None)
            if label:
                label.setText("")
        # --- END ADD ---

    @Slot(QImage)
    def on_frame_ready(self, image: QImage):
        self.ui.live_camera.setPixmap(QPixmap.fromImage(image))

    def filter_unique_labels(self, detections) -> list[str]:
        seen = set()
        unique_labels: list[str] = []
        for d in detections:
            if isinstance(d, str):
                label = d
            elif isinstance(d, dict):
                label = d.get("label")
            else:
                label = None
            if not label:
                continue
            if label not in seen:
                seen.add(label)
                unique_labels.append(label)
        return unique_labels
    
    @Slot(list)
    def on_detections_ready(self, names: list):
        # --- MODIFIED: Stop processing immediately if flag is set ---
        # This check is now the VERY first thing.
        if not self._listing_enabled or self._pause_listing:
            return
        
        # Rate-limiting
        current_time = time.time()
        if current_time - getattr(self, "_last_inference_update", 0.0) < 0.5:
            return
        self._last_inference_update = current_time

        unique_names = self.filter_unique_labels(names)
        text = ", ".join(unique_names) if unique_names else "No detections"

        # --- START: DATABASE SAVE LOGIC ---
        
        # Check if the last save is still running
        if self._bg_save_thread and self._bg_save_thread.is_alive():
            print("Skipping stripe save, previous save still in progress.")
            # We return, but we must also NOT append to the history
            return 

        operator = self.ui.operator_lineEdit.text().strip()
        mag_from = self.ui.magazine_from.text().strip()
        mag_to = self.ui.magazine_to.text().strip()
        
        if not operator or not mag_from or not mag_to:
            self._pause_listing = True 
            self._operation_state = 'idle'
            print("Pausing: Missing Operator/Magazine info.")
            QMessageBox.warning(self, "Missing Info", "Operation paused. Please fill in Operator and Magazine fields to resume.")
            return

        # Start the background save
        self._bg_save_thread = threading.Thread(
            target=self._save_stripe,
            args=(text, operator, mag_from, mag_to),
            daemon=True
        )
        self._bg_save_thread.start()
        # --- END: DATABASE SAVE LOGIC ---


        # --- START: MODIFIED UI DISPLAY LOGIC ---
        
        # **BUG FIX 1: Append to history *before* checking length.**
        # This ensures the UI counter and DB are in sync.
        self._inference_history.append(text) 
        if len(self._inference_history) > 10:
             self._inference_history = self._inference_history[-10:]

        # This block now runs when the 10th item is *added*
        if len(self._inference_history) == 10 and not self._list_full:
            self._inference_history.clear() # Clear for the *next* batch
            self._pause_listing = True
            self._list_full = True
            self.pause_timer.start(3000)
            self._reset_count += 1
            
            print(f"--- UI Package {self._reset_count} complete ---")
            
            label_names = ['one','two','three','four','five','six','seven','eight','nine','ten']
            
            # **BUG FIX 2: Clear labels *after* 3s pause, not before**
            # This logic is moved to self.resume_listing
            
            if self._reset_count >= 20: 
                print(f"--- Magazine complete (20 packages). Stopping operation. ---")
                
                # **BUG FIX 3: Set flag immediately.**
                # This is the fix for the race condition.
                # We set the flag *before* showing the popup.
                self._listing_enabled = False 
                self._operation_state = 'idle'
                self.pause_timer.stop()
                
                self.ui.operator_lineEdit.clear()
                self.ui.magazine_from.clear()
                self.ui.magazine_to.clear()
                
                for label_name in label_names:
                    label = getattr(self.ui, label_name, None)
                    if label:
                        label.setText("")

                QMessageBox.information(self, 
                                        "Operation Complete", 
                                        f"Magazine {self._magazine_run_count} is done processing.")
                return # Stop.

        # Update labels only if not in a "list full" state
        if not self._list_full:
            label_names = ['one','two','three','four','five','six','seven','eight','nine','ten']
            for i, label_name in enumerate(label_names):
                label_widget = getattr(self.ui, label_name, None)
                if not label_widget:
                    continue
                if i < len(self._inference_history):
                    label_widget.setText(self._inference_history[i])
                else:
                    label_widget.setText("")

        QApplication.processEvents()

    def on_export_button_clicked(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Select Export File Type")
        msg_box.setText("Choose the file type for export:")
        excel_button = msg_box.addButton("Excel", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        msg_box.exec()

        if msg_box.clickedButton() == cancel_button:
            return
        
        if msg_box.clickedButton() == excel_button:
            file_filter = "Excel files (*.xlsx)"
            default_ext = ".xlsx"
        else:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Exported File", "", file_filter)
        if not save_path:
            return
        
        if not save_path.lower().endswith(default_ext):
            save_path += default_ext

        try:
            # 1. Fetch data from the database (using the corrected method)
            data = self.capture_db.get_all_capture_data()
            
            if not data:
                QMessageBox.information(self, "Export", "No data found to export.")
                return

            # 2. Create the Excel workbook and worksheet
            workbook = xlsxwriter.Workbook(save_path)
            worksheet = workbook.add_worksheet("Captures")

            # 3. Create a bold format for headers
            header_format = workbook.add_format({'bold': True})

            # 4. Define headers (Corrected to match the new query)
            headers = [
                'Magazine ID', 'Operator', 'Magazine From', 'Magazine To',
                'Package Number', 'Stripe Number', 'Description'
            ]

            # 5. Write headers to the first row
            for col, header_text in enumerate(headers):
                worksheet.write(0, col, header_text, header_format)

            # 6. Write the data rows
            for row, row_data in enumerate(data, start=1):
                for col, cell_data in enumerate(row_data):
                    worksheet.write(row, col, cell_data)
            
            # 7. Adjust column widths for readability
            worksheet.autofit()
            
            # 8. Close the workbook to save the file
            workbook.close()

            QMessageBox.information(self, "Export Successful", f"Data exported successfully to:\n{save_path}")

        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Failed to export data:\n{str(e)}")
        
        return True

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