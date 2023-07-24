from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QGroupBox, \
    QComboBox
from data_manager import DataManager


class PositionAliasWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.position_count: int = 0
        self.member_les: list[QLineEdit] = []
        self.initUI()

    def initUI(self):

        DataManager.add_update_function(self.refresh)

        self.add_btn = QPushButton("직위 추가")
        self.del_btn = QPushButton("직위 삭제")
        self.apply_btn = QPushButton("적용")
        self.cancel_btn = QPushButton("취소")
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidgetLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaWidgetLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        # widget settings
        self.add_btn.pressed.connect(self.add_position_box)
        self.del_btn.pressed.connect(self.remove_position_box)
        for i in range(5):
            self.add_position_box()

        # layouts
        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.add_btn)
        btn_hbox.addWidget(self.del_btn)

        btn_hbox2 = QHBoxLayout()
        btn_hbox2.addWidget(self.apply_btn)
        btn_hbox2.addWidget(self.cancel_btn)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(btn_hbox)
        main_vbox.addWidget(self.scrollArea)
        main_vbox.addLayout(btn_hbox2)

        self.setLayout(main_vbox)

    def refresh(self):
        pass

    def add_position_box(self):
        if self.position_count < 12:
            groupBox = QGroupBox()
            self.scrollAreaWidgetLayout.addWidget(groupBox)
            lb = QLabel(f"{DataManager.position_names[self.position_count]} ->")
            le = QLineEdit()
            self.position_count += 1

            hbox = QHBoxLayout()
            hbox.addWidget(lb)
            hbox.addWidget(le)
            groupBox.setLayout(hbox)

    def remove_position_box(self):
        if self.position_count > 5:
            item = self.scrollAreaWidgetLayout.itemAt(self.position_count - 1)
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeWidget(widget)
            self.position_count -= 1

    def apply_position_alias(self):
        current_guild= DataManager.get_current_guild()
        for i in self.scrollAreaWidgetLayout.count():
            item = self.scrollAreaWidgetLayout.itemAt(i)
            widget: QGroupBox = item.widget()
            layout = widget.layout()
            le_item = layout.itemAt(1)
            le: QLineEdit = le_item.widget()
            alias = le.text()
            position = DataManager.position_names[i]
            eng_position = DataManager.posisiton_kor_to_eng(position)
            current_guild.set_position_alias(position=eng_position, alias=alias)



if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = PositionAliasWidget()
    wg.show()
    sys.exit(app.exec_())
