from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class MyTableWidget(QTableWidget):

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if (e.key() == Qt.Key_C) and e.modifiers() & Qt.ControlModifier:
            pass

