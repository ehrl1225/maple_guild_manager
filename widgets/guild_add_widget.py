from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, \
    QSpinBox, QPushButton
from data_manager import DataManager

class GuildAddWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.guilds_cb = QComboBox()

        self.name_lb = QLabel("길드 이름 :")
        self.name_le = QLineEdit()

        self.server_lb = QLabel("길드 서버 이름 :")
        self.server_le = QLineEdit()

        self.position_count_lb = QLabel("직위 개수")
        self.position_count_sb = QSpinBox()

        self.maple_account_chb = QCheckBox("메이플 계정")

        self.add_btn = QPushButton("add")
        self.del_btn = QPushButton("remove")
        self.cancel_btn = QPushButton("cancel")

        #
        self.refresh_guild_cb()

        self.position_count_sb.setMinimum(5)
        self.position_count_sb.setMaximum(12)

        self.maple_account_chb.released.connect(self.maple_account_chb_work)

        self.add_btn.pressed.connect(self.add_guild)

        #
        self.main_vbox = QVBoxLayout()

        self.main_vbox.addWidget(self.guilds_cb)

        name_hbox = QHBoxLayout()
        name_hbox.addWidget(self.name_lb)
        name_hbox.addWidget(self.name_le)
        self.main_vbox.addLayout(name_hbox)

        server_hbox = QHBoxLayout()
        server_hbox.addWidget(self.server_lb)
        server_hbox.addWidget(self.server_le)
        self.main_vbox.addLayout(server_hbox)

        position_count_hbox = QHBoxLayout()
        position_count_hbox.addWidget(self.position_count_lb)
        position_count_hbox.addWidget(self.position_count_sb)
        self.main_vbox.addLayout(position_count_hbox)

        self.main_vbox.addWidget(self.maple_account_chb)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.add_btn)
        button_hbox.addWidget(self.del_btn)
        button_hbox.addWidget(self.cancel_btn)
        self.main_vbox.addLayout(button_hbox)

        self.setLayout(self.main_vbox)
        self.show()

    def refresh_guild_cb(self):
        self.guilds_cb.clear()
        for g in DataManager.get_data_keys():
            self.guilds_cb.addItem(g)
        self.guilds_cb.addItem("new")

    def guilds_cb_work(self):
        current_guild_name = self.guilds_cb.currentText()
        pass

    def maple_account_chb_work(self):
        if self.maple_account_chb.isChecked():
            self.add_maple_account_box()
        else:
            self.del_maple_account_box()

    def add_maple_account_box(self):
        group_box = QGroupBox()
        self.main_vbox.insertWidget(5, group_box)
        id_lb = QLabel("아이디 :")
        id_le = QLineEdit()
        pw_lb = QLabel("비밀번호 :")
        pw_le = QLineEdit()

        pw_le.setEchoMode(QLineEdit.EchoMode.Password)

        vbox = QVBoxLayout()

        id_hbox = QHBoxLayout()
        id_hbox.addWidget(id_lb)
        id_hbox.addWidget(id_le)
        vbox.addLayout(id_hbox)

        pw_hbox = QHBoxLayout()
        pw_hbox.addWidget(pw_lb)
        pw_hbox.addWidget(pw_le)
        vbox.addLayout(pw_hbox)

        group_box.setLayout(vbox)

    def del_maple_account_box(self):
        item = self.main_vbox.itemAt(5)
        widget = item.widget()
        self.main_vbox.removeWidget(widget)

    def add_guild(self):
        name = self.name_le.text()
        server = self.server_le.text()
        position_count = self.position_count_sb.value()

        if self.maple_account_chb.isChecked():
            item = self.main_vbox.itemAt(5)
            widget: QGroupBox = item.widget()
            layout = widget.layout()
            id_item = layout.itemAt(0)
            id_layout = id_item.layout()
            id_le_item = id_layout.itemAt(1)
            id_widget: QLineEdit = id_le_item.widget()
            id = id_widget.text()
            pw_item = layout.itemAt(1)
            pw_layout = pw_item.layout()
            pw_le_item = pw_layout.itemAt(1)
            pw_widget: QLineEdit = pw_le_item.widget()
            pw = pw_widget.text()
            print(id, pw)




if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = GuildAddWidget()
    sys.exit(app.exec_())