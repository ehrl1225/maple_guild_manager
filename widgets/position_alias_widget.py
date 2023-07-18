from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QGroupBox


class PositionAliasWidget(QWidget):
    position_names = [
                         "길드 마스터",
                         "길드 부마스터"
                     ] + [f"길드 멤버원{n}" for n in range(1, 11)]

    def __init__(self):
        super().__init__()
        self.position_count: int = 0
        self.member_les: list[QLineEdit] = []
        self.initUI()

    def initUI(self):
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

        self.add_btn.pressed.connect(self.add_position_box)
        self.del_btn.pressed.connect(self.remove_position_box)
        for i in range(5):
            self.add_position_box()

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.add_btn)
        btn_hbox.addWidget(self.del_btn)

        btn_hbox2 = QHBoxLayout()
        btn_hbox2.addWidget(self.apply_btn)
        btn_hbox2.addWidget(self.cancel_btn)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(btn_hbox)
        main_vbox.addWidget(self.scrollArea)

        self.setLayout(main_vbox)

        self.show()

    def add_position_box(self):
        if self.position_count < 12:
            groupBox = QGroupBox(self.position_names[self.position_count])
            self.scrollAreaWidgetLayout.addWidget(groupBox)
            lb = QLabel(f"{self.position_names[self.position_count]} ->")
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


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = PositionAliasWidget()
    sys.exit(app.exec_())
