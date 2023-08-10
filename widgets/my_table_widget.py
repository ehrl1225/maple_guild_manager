from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, pyqtSignal

class MyTableWidget(QTableWidget):
    copied = pyqtSignal(list)

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
        selected_items: list[QTableWidgetItem] = self.selectedItems()
        if selected_items:
            self.copied.emit(selected_items)

    def set_divide_chr(self, chr):
        self.divide_chr = chr