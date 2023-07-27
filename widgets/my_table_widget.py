from PyQt5.QtWidgets import QTableWidget, QAbstractItemView
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class MyTableWidget(QTableWidget):

    def __init__(self):
        super().__init__()
        self.divide_chr = "\t"
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if (e.key() == Qt.Key_C) and e.modifiers() & Qt.ControlModifier:
            self.copy()

    def copy(self):
        selected_item = self.selectedItems()
        if selected_item:
            pass

    def set_divide_chr(self, chr):
        self.divide_chr = chr