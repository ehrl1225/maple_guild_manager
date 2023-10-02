from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QGroupBox, \
    QMessageBox
from PyQt5.QtGui import QCloseEvent
from data_manager import DataManager
from typing import Generator


class PositionAliasWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.position_count: int = 0
        self.member_les: list[QLineEdit] = []
        self.changed: bool = False
        self.initUI()

    def initUI(self):

        DataManager.add_update_function(self.refresh)

        self.add_btn = QPushButton("직위 추가")
        self.del_btn = QPushButton("직위 감소")
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidgetLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaWidgetLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        # widget settings
        self.add_btn.pressed.connect(self.add_position_box)
        self.del_btn.pressed.connect(self.del_position_box)
        for i in range(5):
            self.add_position_box()

        # layouts
        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.add_btn)
        btn_hbox.addWidget(self.del_btn)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(btn_hbox)
        main_vbox.addWidget(self.scrollArea)

        self.setLayout(main_vbox)

    def initialize(self):
        for i in range(5, self.position_count):
            self.del_position_box()
        for i in range(5):
            layout = self.scrollAreaWidgetLayout.itemAt(i).widget().layout()
            le: QLineEdit = layout.itemAt(1).widget()
            le.clear()

    def refresh(self):
        if self.position_count < DataManager.get_current_position_length():
            count = DataManager.get_current_position_length() - self.position_count
            for _ in range(count):
                self.del_position_box()
        elif self.position_count > DataManager.get_current_position_length():
            count = self.position_count
            for _ in range(count):
                self.add_position_box()
        for i in range(self.position_count):
            item = self.scrollAreaWidgetLayout.itemAt(i)
            group_box = item.widget()
            layout = group_box.layout()
            le: QLineEdit = layout.itemAt(1).widget()
            alias = DataManager.get_position_alias(DataManager.get_position_name(index=i))
            le.setText(alias)

    def get_data(self, index: int) -> str:
        if index < self.scrollAreaWidgetLayout.count():
            item = self.scrollAreaWidgetLayout.itemAt(index)
            group_box = item.widget()
            layout = group_box.layout()
            le: QLineEdit = layout.itemAt(1).widget()
            return le.text()

    def check_change(self) -> None:
        if self.position_count > 0:
            if self.position_count == DataManager.get_current_position_length():
                data = [self.get_data(i) for i in range(self.position_count)]
                for i in range(self.position_count):
                    alias = DataManager.get_position_alias(DataManager.get_position_name(index=i))
                    if data[i] != alias:
                        break
                else:
                    self.changed = False
                self.changed = True

    def add_position_box(self):
        if self.position_count < 12:
            groupBox = QGroupBox()
            self.scrollAreaWidgetLayout.addWidget(groupBox)
            lb = QLabel(f"{DataManager.position_names[self.position_count]} ->")
            le = QLineEdit()
            self.position_count += 1

            le.textChanged.connect(self.check_change)

            hbox = QHBoxLayout()
            hbox.addWidget(lb)
            hbox.addWidget(le)
            groupBox.setLayout(hbox)

            self.check_change()

    def del_position_box(self):
        if self.position_count > 5:
            item = self.scrollAreaWidgetLayout.itemAt(self.position_count - 1)
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeWidget(widget)
            self.position_count -= 1

            self.check_change()

    def apply_position_alias(self):
        current_guild = DataManager.get_current_guild()
        for i in range(self.scrollAreaWidgetLayout.count()):
            item = self.scrollAreaWidgetLayout.itemAt(i)
            widget: QGroupBox = item.widget()
            layout = widget.layout()
            le_item = layout.itemAt(1)
            le: QLineEdit = le_item.widget()
            alias = le.text()
            if alias!="":
                position = DataManager.position_names[i]
                eng_position = DataManager.posisiton_kor_to_eng(position)
                DataManager.set_guild_position_alias(
                    server=current_guild.server,
                    name=current_guild.name,
                    position=eng_position,
                    alias=alias
                )

    def cancel_position_alias(self):
        self.refresh()
        self.close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.changed:
            # reply = QMessageBox.warning(
            #     self,
            #     "경고",
            #     "적용하지 않았는데 적용하시겠습니까?",
            #     buttons=QMessageBox.Yes| QMessageBox.No | QMessageBox.Cancel,
            #     defaultButton=QMessageBox.No
            # )
            # if reply == QMessageBox.Cancel:
            #     a0.ignore()
            # else:
            #     if reply == QMessageBox.Yes:
            #         self.apply_position_alias()
            #     elif reply == QMessageBox.No:
            #         self.refresh()
            #     else:
            #         pass
            #     self.changed = False
            a0.accept()
        else:
            a0.accept()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = PositionAliasWidget()
    wg.show()
    sys.exit(app.exec_())
