from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox
from data_manager import DataManager

class GuildAddWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.guilds_cb = QComboBox()

        self.name_lb = QLabel()
        self.name_le = QLineEdit()

        self.server_lb = QLabel()
        self.server_le = QLineEdit()

        self.position_count_lb = QLabel()
        self.position_count_cb = QComboBox()

        self.maple_account_chb = QCheckBox()


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
        position_count_hbox.addWidget(self.position_count_cb)
        self.main_vbox.addLayout(position_count_hbox)

        self.main_vbox.addWidget(self.maple_account_chb)

        self.setLayout(self.main_vbox)
        self.show()

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
        id_lb = QLabel()
        id_le = QLineEdit()
        pw_lb = QLabel()
        pw_le = QLineEdit()

        pw_le.setEchoMode(QLineEdit_EchoMode=QLineEdit.EchoMode.PasswordEchoOnEdit)

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
