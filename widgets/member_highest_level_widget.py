from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLineEdit, QComboBox, QHBoxLayout, QPushButton
from  functools import partial

class MemberHighestLevelWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidgetLayout = QVBoxLayout()
        self.scrollAreaWidget.setLayout(self.scrollAreaWidgetLayout)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.add_btn = QPushButton("add")
        self.member_layouts: list[QHBoxLayout] = list()

        main_vbox = QVBoxLayout()
        main_vbox.addWidget(self.add_btn)
        main_vbox.addWidget(self.scrollArea)

        self.add_btn.pressed.connect(self.add_highest_level_member)

        self.setLayout(main_vbox)
        self.show()

    def add_highest_level_member(self):
        group_box = QGroupBox()
        self.scrollAreaWidgetLayout.addWidget(group_box)
        le = QLineEdit()
        cb = QComboBox()
        btn = QPushButton("X")

        hbox = QHBoxLayout()
        hbox.addWidget(le)
        hbox.addWidget(cb)
        hbox.addWidget(btn)
        index = self.scrollAreaWidgetLayout.count() - 1
        btn.pressed.connect(partial(self.remove_highest_level_member, index))
        self.member_layouts.append(hbox)

        group_box.setLayout(hbox)

    def remove_highest_level_member(self, index=-1):
        if self.scrollAreaWidgetLayout.count() > 0:
            last_index = self.scrollAreaWidgetLayout.count() - 1
            if index == -1:
                index = last_index
            if self.scrollAreaWidgetLayout.count() >= 2:
                for i, m in enumerate(self.member_layouts[index : last_index]):
                    i = i + index
                    le: QLineEdit = m.itemAt(0).widget()
                    cb: QComboBox = m.itemAt(1).widget()
                    next_member = self.member_layouts[i+1]
                    next_le: QLineEdit = next_member.itemAt(0).widget()
                    next_cb: QComboBox = next_member.itemAt(1).widget()
                    le.setText(next_le.text())
                    cb.setCurrentIndex(next_cb.currentIndex())

            item = self.scrollAreaWidgetLayout.itemAt(last_index)
            del self.member_layouts[last_index]
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeWidget(widget)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    wg = MemberHighestLevelWidget()
    sys.exit(app.exec_())