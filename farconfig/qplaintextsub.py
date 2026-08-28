from PySide6.QtWidgets import  QPlainTextEdit
from PySide6.QtCore import Qt

class QPlainTextSub(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnPressedCallback = None

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            #print("Return pressed")
            if (self.returnPressedCallback is not None):
                self.returnPressedCallback(self)
            event.accept()
            return
        # Call base class for all other keys (handles normal typing)
        super().keyPressEvent(event)

    def setText(self, text):
        self.setPlainText(text)

    def text(self):
        return self.toPlainText()

    def connectReturnPressed(self, callback):
        self.returnPressedCallback = callback