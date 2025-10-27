# camera_module.py
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
import cv2

class CameraThread(QThread):
    """Thread that captures frames from OpenCV and emits QImage frames."""
    frame_ready = Signal(QImage)

    def __init__(self, camera_index: int = 0, fps: int = 30, width: int | None = None, height: int | None = None, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.fps = max(1, int(fps))
        self.width = width
        self.height = height
        self._running = False
        self.latest_frame = None  # Add attribute to store latest raw frame

    def run(self):
        self._running = True
        cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW) if hasattr(cv2, 'CAP_DSHOW') else cv2.VideoCapture(self.camera_index)
        if self.width:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.width))
        if self.height:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.height))

        delay_ms = int(1000 / self.fps)

        while self._running:
            ret, frame = cap.read()
            if not ret:
                self.msleep(50)
                continue

            self.latest_frame = frame.copy()  # Store the raw frame here

            # Convert BGR -> RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w

            qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
            self.frame_ready.emit(qimg)
            self.msleep(delay_ms)

        cap.release()

    def stop(self):
        self._running = False
        self.wait()
