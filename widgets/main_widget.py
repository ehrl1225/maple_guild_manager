from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tb = QTableWidget()

        vbox = QVBoxLayout()
