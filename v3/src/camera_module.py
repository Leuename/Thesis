import cv2
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from ultralytics import YOLO
import torch


class CameraInferenceThread(QThread):
    """
    Thread that captures camera frames and runs YOLO inference asynchronously.
    Emits signals for frame display, detection names, and box info.
    
    Usage:
    - Instantiate with camera index, model path, and optional confidence threshold.
    - Connect signals: frame_ready(QImage), detections_ready(list of str), boxes_ready(list of dict).
    - Call start() to begin and stop() to end safely.
    """
    
    frame_ready = Signal(QImage)          # Current frame (RGB) as QImage for GUI display
    detections_ready = Signal(list)       # List of detected class names (strings)
    boxes_ready = Signal(list)             # List of dicts per box, e.g. {'xyxy': (x1,y1,x2,y2), 'cls': int, 'conf': float}
    
    def __init__(self, camera_index: int, model_path: str, conf_thresh: float = 0.25, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.model_path = model_path
        self.conf_thresh = conf_thresh
        self._running = False

        # Load YOLO model on proper device (CUDA if available)
        self.model = YOLO(self.model_path)
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.conf = self.conf_thresh  # Set confidence threshold
        
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            # Emit empty signals or log error - here just stop thread
            print(f"[CameraInferenceThread] Error: Cannot open camera index {self.camera_index}")
            return
        
        self._running = True
        
        while self._running:
            ret, frame = self.cap.read()
            if not ret:
                # Failed frame capture: wait briefly and retry
                time.sleep(0.05)
                continue
            
            # Run inference on current frame with no verbose output
            results = self.model(frame, verbose=False)[0]
            
            # Extract detection boxes where confidence > conf_thresh (already handled internally)
            boxes = results.boxes
            names = []
            boxes_info = []
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    cls = int(box.cls.item())
                    conf = float(box.conf.item())
                    xyxy = tuple(map(float, box.xyxy[0].tolist()))
                    names.append(self.model.names[cls])
                    boxes_info.append({'xyxy': xyxy, 'cls': cls, 'conf': conf})
            else:
                names = []
                boxes_info = []

            # Annotate frame with box overlays
            annotated_frame = results.plot()  # This returns a numpy BGR image with overlays

            # Convert annotated BGR frame to RGB for Qt
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Emit signals to GUI
            self.frame_ready.emit(qt_image)
            self.detections_ready.emit(names)
            self.boxes_ready.emit(boxes_info)

            # Throttle loop to avoid 100% CPU usage (~30 FPS max)
            time.sleep(0.03)

        # Cleanup camera on exit
        self.cap.release()

    def stop(self):
        """Stop the thread and release camera resource safely."""
        self._running = False
        self.wait()
