from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QGraphicsOpacityEffect,
)
import sys


class SplashScreen(QWidget):
    """A simple splash screen that animates a logo label (slide + fade)
    and then opens the main window.

    Behavior:
    - Logo starts off-screen on the left
    - Slides in to center using a QPropertyAnimation (geometry)
    - Fades in concurrently using QGraphicsOpacityEffect
    - Pauses for a moment, then fades out and emits finished signal
    """

    def __init__(self, parent=None, duration_show=2200):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.duration_show = duration_show

        # Appearance
        self.resize(560, 320)

        container = QWidget(self)
        container.setObjectName("container")
        container.setStyleSheet(
            "#container{background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0f2027, stop:1 #203a43);"
            "border-radius:16px;}"
        )
        container.setGeometry(20, 20, 520, 280)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(6)

        # 'Logo' label (text-based so no extra image files required)
        self.logo = QLabel("MyApp")
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet(
            "font: 700 44px 'Segoe UI', Arial; color: white; letter-spacing: 2px;"
        )
        layout.addStretch()
        layout.addWidget(self.logo)
        layout.addStretch()

        # Add a small tagline
        tag = QLabel("Loading…")
        tag.setAlignment(Qt.AlignCenter)
        tag.setStyleSheet("font: 12px 'Segoe UI'; color: rgba(255,255,255,0.8);")
        layout.addWidget(tag)

        # Keep the label off-screen initially (we'll animate geometry)
        self._init_positions()

        # Opacity effect for fade-in/out
        self.opacity_effect = QGraphicsOpacityEffect(self.logo)
        self.logo.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        # Animations
        self.anim_move = QPropertyAnimation(self.logo, b"geometry", self)
        self.anim_move.setEasingCurve(QEasingCurve.OutBack)
        self.anim_move.setDuration(900)

        self.anim_fade_in = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.anim_fade_in.setDuration(700)
        self.anim_fade_in.setStartValue(0.0)
        self.anim_fade_in.setEndValue(1.0)

        self.anim_fade_out = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.anim_fade_out.setDuration(600)
        self.anim_fade_out.setStartValue(1.0)
        self.anim_fade_out.setEndValue(0.0)

        # Sequence: move+fade-in -> wait -> fade-out -> finished
        self.anim_move.finished.connect(self._on_move_finished)
        self.anim_fade_out.finished.connect(self._on_finish)

        # Center window on screen
        self._center_on_screen()

    def _init_positions(self):
        # We'll animate the geometry of the logo label relative to container
        container_geom = QRect(40, 40, 440, 200)  # approximate area inside container
        # final geometry (centered)
        final_w = 300
        final_h = 80
        final_x = int((520 - final_w) / 2) + 20
        final_y = int((280 - final_h) / 2) + 20
        self.final_geom = QRect(final_x, final_y, final_w, final_h)

        # start geometry is off-screen to the left
        start_x = -final_w
        self.start_geom = QRect(start_x, final_y, final_w, final_h)

        # put the logo initially at start_geom so animation begins from there
        self.logo.setGeometry(self.start_geom)

    def _center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        center_x = (screen.width() - self.width()) // 2
        center_y = (screen.height() - self.height()) // 2
        self.move(center_x, center_y)

    def start(self):
        # Kick off move and fade-in together
        self.anim_move.setStartValue(self.start_geom)
        self.anim_move.setEndValue(self.final_geom)
        self.anim_move.setDuration(900)

        self.anim_fade_in.setStartValue(0.0)
        self.anim_fade_in.setEndValue(1.0)
        self.anim_fade_in.setDuration(700)

        self.anim_move.start()
        self.anim_fade_in.start()

    def _on_move_finished(self):
        # After move + fade-in, wait a bit then fade out
        QTimer.singleShot(self.duration_show - 900, self._start_fade_out)

    def _start_fade_out(self):
        self.anim_fade_out.start()

    def _on_finish(self):
        # Hide splash and notify (we'll just create/show main window externally)
        self.hide()
        self.deleteLater()
        # emit an event by posting a custom event on the app object or call a callback.
        # For simplicity we'll set an attribute on QApplication for the main code to watch.
        QApplication.instance().splash_done = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 520)
        label = QLabel("This is the main window.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font: 18px 'Segoe UI';")
        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)
    # Small flag used to communicate when splash finishes
    app.splash_done = False

    splash = SplashScreen(duration_show=2000)
    splash.show()
    splash.start()

    # Poll for the flag set by the splash when it finishes. Using a QTimer avoids blocking.
    main_win = MainWindow()

    def check_and_show():
        if getattr(app, "splash_done", False):
            main_win.show()
            poller.stop()

    poller = QTimer()
    poller.timeout.connect(check_and_show)
    poller.start(80)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
