import sys

from widgets.spreadsheet_thread import SpreadsheetThread

# os.chdir("..")
from PyQt5.QtGui import QColor, QCloseEvent
from PyQt5.QtWidgets import QWidget, QComboBox, QTableWidget, QLineEdit, QPushButton, QSpinBox, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLabel, QApplication
from spreadsheet_api import SpreadsheetManager
from data_manager import DataManager


class SpreadsheetWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.spread_manager = SpreadsheetManager()
        self.st = SpreadsheetThread()
        self.initUI()

    def initUI(self):
        self.url_le = QLineEdit()
        self.url_btn = QPushButton("링크 불러오기")
        self.title_cb = QComboBox()
        self.row_lb = QLabel("행(숫자)")
        self.row_le = QLineEdit()
        self.col_lb = QLabel("열(알파벳)")
        self.col_le = QLineEdit()
        self.data_btn = QPushButton("불러오기")
        self.direction_cb = QComboBox()
        self.preview_table = QTableWidget()
        self.apply_btn = QPushButton("적용")

        url = DataManager.load_spreadsheet_url()
        if url != None:
            self.url_le.setText(url)

        self.url_btn.pressed.connect(lambda : self.st.queue.append(self.load_url))

        self.title_cb.currentIndexChanged.connect(self.set_title)

        self.data_btn.pressed.connect(lambda : self.st.queue.append(self.load_data))

        self.direction_cb.addItem("가로")
        self.direction_cb.addItem("세로")
        self.direction_cb.currentIndexChanged.connect(self.paint_line)

        self.apply_btn.pressed.connect(self.apply)

        vbox =QVBoxLayout()

        url_hbox = QHBoxLayout()
        url_hbox.addWidget(self.url_le)
        url_hbox.addWidget(self.url_btn)
        vbox.addLayout(url_hbox)
        vbox.addWidget(self.title_cb)

        data_hbox = QHBoxLayout()
        data_hbox.addWidget(self.preview_table)

        load_vbox = QVBoxLayout()

        load_vbox.addWidget(self.data_btn)

        row_hbox =QHBoxLayout()
        row_hbox.addWidget(self.row_lb)
        row_hbox.addWidget(self.row_le)
        load_vbox.addLayout(row_hbox)

        col_hbox = QHBoxLayout()
        col_hbox.addWidget(self.col_lb)
        col_hbox.addWidget(self.col_le)
        load_vbox.addLayout(col_hbox)

        load_vbox.addWidget(self.direction_cb)

        load_vbox.addWidget(self.apply_btn)

        data_hbox.addLayout(load_vbox)

        self.st.start()

        vbox.addLayout(data_hbox)
        self.setLayout(vbox)

    def apply(self):
        row_le_text = self.row_le.text()
        col_le_text = self.col_le.text()
        col = self.spread_manager.get_col_to_num(col_le_text)
        if row_le_text.isdecimal():
            row = int(row_le_text)
        else:
            return
        if col == -1:
            return
        data = DataManager.get_filtered_data(self.direction_cb.currentText())
        self.spread_manager.update_data(
            row=row,
            col=col,
            data=data
        )

    def load_url(self):
        url = self.url_le.text()
        result = self.spread_manager.open_by_url(url)

        if result== -1:
            print("error")
            return
        elif result == 0:
            self.title_cb.currentIndexChanged.disconnect(self.set_title)
            self.get_titles()
            self.title_cb.currentIndexChanged.connect(self.set_title)
            title = self.title_cb.currentText()
            self.spread_manager.get_worksheet(title)
            DataManager.save_spreadsheet_url(url)

    def get_titles(self):
        self.title_cb.clear()
        for t in self.spread_manager.get_titles():
            self.title_cb.addItem(t)

    def set_title(self):
        title = self.title_cb.currentText()
        self.spread_manager.get_worksheet(title)

    def load_data(self):
        row_le_text =self.row_le.text()
        col_le_text = self.col_le.text()
        col = self.spread_manager.get_col_to_num(col_le_text)
        if row_le_text.isdecimal():
            row = int(row_le_text)
        else:
            return
        if col == -1:
            return

        data = self.spread_manager.get_data(row, col)
        self.preview_table.clear()
        self.preview_table.setRowCount(10)
        self.preview_table.setColumnCount(10)
        self.preview_table.setHorizontalHeaderLabels(self.spread_manager.get_horizontal_headers(col))
        self.preview_table.setVerticalHeaderLabels(self.spread_manager.get_vertical_header(row))
        for i in range(10):
            for j in range(10):
                tw_item = QTableWidgetItem(data[i][j])
                self.preview_table.setItem(row, col, tw_item)

        for row,line in enumerate(data):
            for col,item in enumerate(line):
                tw_item = QTableWidgetItem(item)
                self.preview_table.setItem(row,col,tw_item)
        self.paint_line()

    def paint_line(self):
        self.preview_table.item(1,1).setBackground(QColor(11,120,168))
        direction = self.direction_cb.currentText()
        if direction=="가로":
            for i in range(2,10):
                self.preview_table.item(1, i).setBackground(QColor(61, 199, 5))
            for i in range(2, 10):
                self.preview_table.item(i, 1).setBackground(QColor(255, 255, 255))
        if direction=="세로":
            for i in range(2, 10):
                self.preview_table.item(i, 1).setBackground(QColor(61, 199, 5))
            for i in range(2,10):
                self.preview_table.item(1, i).setBackground(QColor(255, 255,255))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.st.go = False
        a0.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wg = SpreadsheetWidget()
    wg.show()
    sys.exit(app.exec_())