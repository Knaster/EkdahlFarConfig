import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PySide6.QtCore import QTimer, Qt

class ProgressDialog(QDialog):
    def __init__(self, duration=5000, title="Calibrating", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(300, 100)

        self.duration = duration  # Duration in milliseconds
        self.elapsed = 0

        # Create layout and widgets
        layout = QVBoxLayout(self)
        self.label = QLabel("Please wait...", self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)

        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)

        # Timer for updating progress
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timeOut = False

    def start(self, timeOut = False):
        self.timeOut = timeOut
        self.timer.start(100)  # Update every 100 ms
        self.exec()  # Block until the dialog is closed

    def update_progress(self):
        self.elapsed += 100
        progress = int((self.elapsed / self.duration) * 100)
        self.progressBar.setValue(progress)

        if self.elapsed >= self.duration:
            self.elapsed = 0
            if self.timeOut:
                self.timer.stop()
                self.accept()  # Close the dialog


    def stop(self):
        self.timer.stop()
        self.accept()


def show_blocking_progress_bar():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    dialog = ProgressDialog(3000)
    dialog.start()

