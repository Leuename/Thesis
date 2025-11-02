# camera_module.py
from __future__ import annotations
import queue
import numpy as np
import cv2
from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QThread, QObject
from PySide6.QtGui import QImage

# ---------- Camera thread (captures frames and emits both QImage and raw BGR numpy) ----------
class CameraThread(QThread):
    """
    Thread that captures frames from OpenCV and emits:
      - frame_qimage_ready (QImage)  : for backward compatibility / preview UI
      - raw_frame_ready (np.ndarray) : BGR image (H, W, 3) for inference worker (model expects BGR)
    """
    frame_qimage_ready = QtCore.Signal(QImage)
    raw_frame_ready = QtCore.Signal(object)  # emits BGR numpy array

    def __init__(self, camera_index: int = 0, fps: int = 30, width: Optional[int] = None, height: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.fps = max(1, int(fps))
        self.width = width
        self.height = height
        self._running = False
        self.latest_frame: Optional[np.ndarray] = None  # BGR

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
                # small sleep to avoid busy loop when camera fails
                self.msleep(50)
                continue

            # ensure we keep our own copy (thread-safety)
            self.latest_frame = np.ascontiguousarray(frame).copy()

            # Emit raw BGR frame for inference worker
            try:
                self.raw_frame_ready.emit(self.latest_frame)
            except Exception:
                # defensive: signals sometimes can fail if UI is tearing down
                pass

            # Also emit a QImage for immediate preview in UI (RGB)
            try:
                rgb = cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
                self.frame_qimage_ready.emit(qimg)
            except Exception:
                # Ignore QImage conversion errors, continue capturing
                pass

            self.msleep(delay_ms)

        cap.release()

    def stop(self):
        self._running = False
        self.wait()


# ---------- Inference runnable + emitter (works with QThreadPool) ----------
class FrameSignalEmitter(QObject):
    """QObject that owns signals for threadpool-runner to emit annotated frames (RGB numpy)."""
    frame_ready = QtCore.Signal(object)  # annotated RGB numpy array


class InferenceRunnable(QtCore.QRunnable):
    """
    QRunnable that loops reading frames from an internal single-slot queue and runs model inference.
    - setAutoDelete(False) so it persists as a long-running runnable inside the thread pool.
    - Use `submit_frame(frame)` from the GUI thread to supply new frames (BGR ndarray).
    """
    def __init__(self, model, signal_emitter: FrameSignalEmitter):
        super().__init__()
        self.model = model
        self.signals = signal_emitter
        self._running = True
        self.frames_queue: "queue.Queue[np.ndarray]" = queue.Queue(maxsize=1)
        self.setAutoDelete(False)

    def submit_frame(self, frame: np.ndarray):
        """
        Called from GUI thread. Keeps only the most recent frame (replace old if queue full).
        Frame should be BGR (model expectation).
        """
        if frame is None:
            return
        # make contiguous copy to avoid memory/view issues
        frame_to_put = np.ascontiguousarray(frame)
        try:
            if self.frames_queue.full():
                try:
                    self.frames_queue.get_nowait()
                except queue.Empty:
                    pass
            self.frames_queue.put_nowait(frame_to_put)
        except queue.Full:
            # extremely unlikely because we removed one above; ignore
            pass

    def run(self):
        while self._running:
            try:
                frame = self.frames_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Defensive: ensure correct dtype & contiguity
            frame = np.ascontiguousarray(frame)
            # Do inference
            try:
                # NOTE: your model may expect different input pre-processing.
                # Provide BGR frame directly if model was trained with OpenCV BGR images.
                results = self.model(frame)[0]
                annotated = results.plot()
            except Exception as e:
                # On error, fall back to original frame (so UI still shows something)
                print("Inference/plot error:", e)
                annotated = frame

            # Normalize dtype if float
            if np.issubdtype(getattr(annotated, "dtype", np.uint8), np.floating):
                try:
                    annotated = np.clip(annotated * 255.0, 0, 255).astype(np.uint8)
                except Exception:
                    annotated = annotated.astype(np.uint8, copy=False)

            elif annotated.dtype != np.uint8:
                try:
                    annotated = annotated.astype(np.uint8)
                except Exception:
                    annotated = np.ascontiguousarray(annotated)

            # Ensure contiguous
            annotated = np.ascontiguousarray(annotated)

            # Convert to RGB numpy image (H, W, 3)
            rgb = None
            try:
                if annotated.ndim == 3:
                    c = annotated.shape[2]
                    if c == 3:
                        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                    elif c == 4:
                        # BGRA -> RGBA -> RGB (drop alpha)
                        rgba = cv2.cvtColor(annotated, cv2.COLOR_BGRA2RGBA)
                        rgb = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
                    elif c == 1:
                        rgb = cv2.cvtColor(annotated, cv2.COLOR_GRAY2RGB)
                    else:
                        # unknown channels -> try BGR->RGB
                        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                elif annotated.ndim == 2:
                    rgb = cv2.cvtColor(annotated, cv2.COLOR_GRAY2RGB)
                else:
                    # unexpected shape: fallback to black frame
                    h, w = (480, 640)
                    rgb = np.zeros((h, w, 3), dtype=np.uint8)
            except Exception as e:
                print("Conversion to RGB error:", e)
                # fallback to converting original frame to RGB (assuming original was BGR)
                try:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except Exception:
                    rgb = np.zeros((480, 640, 3), dtype=np.uint8)

            # Final safety: contiguous uint8
            rgb = np.ascontiguousarray(rgb)
            if rgb.dtype != np.uint8:
                rgb = np.clip(rgb, 0, 255).astype(np.uint8)

            # Emit RGB numpy array — receiver should convert to QImage (GUI thread)
            try:
                self.signals.frame_ready.emit(rgb)
            except Exception:
                # ignore signal emission errors during teardown
                pass

    def stop(self):
        self._running = False
        # empty queue to unblock quickly
        try:
            while not self.frames_queue.empty():
                self.frames_queue.get_nowait()
        except Exception:
            pass


# ---------- Small manager helper to create/start/stop the runnable cleanly ----------
class InferenceManager:
    """
    Helper that owns the FrameSignalEmitter + InferenceRunnable and starts it
    in the global QThreadPool. Use `submit(frame_bgr)` to feed frames.
    """
    def __init__(self, model):
        self.signals = FrameSignalEmitter()
        self.runnable = InferenceRunnable(model, self.signals)
        self.pool = QtCore.QThreadPool.globalInstance()
        self.started = False

    def start(self):
        if not self.started:
            self.pool.start(self.runnable)
            self.started = True

    def submit(self, frame_bgr: np.ndarray):
        if not self.started:
            # start lazily if needed
            self.start()
        self.runnable.submit_frame(frame_bgr)

    def stop(self):
        try:
            self.runnable.stop()
        finally:
            self.started = False
