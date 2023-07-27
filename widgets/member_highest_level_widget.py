from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLineEdit, QComboBox, QHBoxLayout, QPushButton
from functools import partial
from data_manager import DataManager


class MemberHighestLevelWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self) -> None:

        DataManager.add_update_function(self.refresh)

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

    def refresh(self) -> None:
        for _ in range(self.scrollAreaWidgetLayout.count()):
            self.del_highest_level_member()
        data: dict[str, str] = DataManager.get_current_highest_level_members()
        positions: list[str] = DataManager.get_current_available_positions()
        for i, d in enumerate(data):
            self.add_highest_level_member()
            item = self.scrollAreaWidgetLayout.itemAt(i)
            group_box = item.widget()
            layout = group_box.layout()
            le_item = layout.itemAt(0)
            le: QLineEdit = le_item.widget()
            le.setText(d)
            cb_item = layout.itemAt(1)
            cb: QComboBox = cb_item.widget()
            index = positions.index(data[d])
            cb.setCurrentIndex(index)

    def add_highest_level_member(self) -> None:
        group_box: QGroupBox = QGroupBox()
        self.scrollAreaWidgetLayout.addWidget(group_box)
        le: QLineEdit = QLineEdit()
        cb: QComboBox = QComboBox()
        btn: QPushButton = QPushButton("X")

        for p in DataManager.get_current_guild().get_available_positions():
            cb.addItem(p)

        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addWidget(le)
        hbox.addWidget(cb)
        hbox.addWidget(btn)
        index = self.scrollAreaWidgetLayout.count() - 1
        btn.pressed.connect(partial(self.del_highest_level_member, index))
        self.member_layouts.append(hbox)

        group_box.setLayout(hbox)

    def del_highest_level_member(self, index=-1) -> None:
        if self.scrollAreaWidgetLayout.count() > 0:
            last_index = self.scrollAreaWidgetLayout.count() - 1
            if index == -1:
                index = last_index
            if self.scrollAreaWidgetLayout.count() >= 2:
                for i, m in enumerate(self.member_layouts[index: last_index]):
                    i = i + index
                    le: QLineEdit = m.itemAt(0).widget()
                    cb: QComboBox = m.itemAt(1).widget()
                    next_member = self.member_layouts[i + 1]
                    next_le: QLineEdit = next_member.itemAt(0).widget()
                    next_cb: QComboBox = next_member.itemAt(1).widget()
                    le.setText(next_le.text())
                    cb.setCurrentIndex(next_cb.currentIndex())

            item = self.scrollAreaWidgetLayout.itemAt(last_index)
            del self.member_layouts[last_index]
            widget = item.widget()
            self.scrollAreaWidgetLayout.removeWidget(widget)

    def apply_changes(self) -> None:
        DataManager.clear_current_highest_level_members()
        if self.scrollAreaWidgetLayout.count() > 0:
            for i in range(1, self.scrollAreaWidgetLayout.count()):
                item = self.scrollAreaWidgetLayout.itemAt(i)
                layout = item.layout()
                le_item = layout.itemAt(0)
                le: QLineEdit = le_item.widget()
                name = le.text()
                cb_item = layout.itemAt(1)
                cb: QComboBox = cb_item.widget()
                position = cb.currentIndex()
                DataManager.add_current_highest_level_member(name=name, position=position)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = MemberHighestLevelWidget()
    wg.show()
    sys.exit(app.exec_())
