from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget
from my_table_widget import MyTableWidget
from data_manager import DataManager

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tb = QTableWidget()

        vbox = QVBoxLayout()

        self.setLayout(vbox)

    def refresh_tb(self):
        self.tb.clear()
