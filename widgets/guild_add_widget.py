from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, \
    QSpinBox, QPushButton, QCompleter
from PyQt5.QtCore import QStringListModel
from data_manager import DataManager
from position_alias_widget import PositionAliasWidget
from member_highest_level_widget import MemberHighestLevelWidget
from guild_update_setting_widget import GuildUpdateSettingWidget

server_name = [
    "루나", "luna",
    "스카니아", "scania",
    "엘리시움", "elysium",
    "크로아", "croa",
    "오로라", "aurora",
    "제니스", "zenith",
    "이노시스", "enosis",
    "아케인", "arcane",
    "노바", "nova",
    "레드", "red",
    "베라", "bera",
    "유니온", "union",
    "리부트", "reboot",
    "리부트2", "reboot2"
]

class GuildAddWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        DataManager.add_update_function(self.refresh_guild_cb)

        self.guild_server_cb = QComboBox()
        self.guild_name_cb = QComboBox()

        self.name_lb = QLabel("길드 이름 :")
        self.name_le = QLineEdit()

        self.server_lb = QLabel("길드 서버 이름 :")
        self.server_le = QLineEdit()
        self.server_model = QStringListModel()
        self.server_model.setStringList(server_name)
        self.server_completer = QCompleter()
        self.server_completer.setModel(self.server_model)
        self.server_le.setCompleter(self.server_completer)

        self.position_count_lb = QLabel("직위 개수")
        self.position_count_sb = QSpinBox()

        self.maple_account_chb = QCheckBox("메이플 계정")
        self.position_alias_chb = QCheckBox("직위 별명 설정")
        self.member_highest_level_chb = QCheckBox("멤버 최고 레벨 저장")
        self.guild_update_setting_chb = QCheckBox("길드 정보 업데이트 요소")


        self.add_btn = QPushButton("add")
        self.del_btn = QPushButton("remove")
        self.cancel_btn = QPushButton("cancel")

        self.pa_wg = PositionAliasWidget()
        self.mhl_wg = MemberHighestLevelWidget()
        self.gus_wg = GuildUpdateSettingWidget()

        #
        self.refresh_guild_cb()

        self.position_count_sb.setMinimum(5)
        self.position_count_sb.setMaximum(12)

        self.maple_account_chb.released.connect(self.maple_account_chb_work)
        self.position_alias_chb.released.connect(self.position_alias_chb_work)
        self.member_highest_level_chb.released.connect(self.member_highest_level_chb_work)
        self.guild_update_setting_chb.released.connect(self.guild_update_setting_chb_work)

        self.add_btn.pressed.connect(self.add_guild)

        #
        self.main_vbox = QVBoxLayout()

        guild_hbox = QHBoxLayout()
        guild_hbox.addWidget(self.guild_server_cb)
        guild_hbox.addWidget(self.guild_name_cb)
        self.main_vbox.addLayout(guild_hbox)

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

        self.main_vbox.addWidget(self.position_alias_chb)

        self.main_vbox.addWidget(self.member_highest_level_chb)

        self.main_vbox.addWidget(self.guild_update_setting_chb)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.add_btn)
        button_hbox.addWidget(self.del_btn)
        button_hbox.addWidget(self.cancel_btn)
        self.main_vbox.addLayout(button_hbox)

        self.setLayout(self.main_vbox)

    def position_alias_chb_work(self):
        if self.position_alias_chb.isChecked():
            index = self.main_vbox.indexOf(self.position_alias_chb)
            self.main_vbox.insertWidget(index + 1, self.pa_wg)
            self.pa_wg.adjustSize()
            self.pa_wg.show()
        else:
            self.main_vbox.removeWidget(self.pa_wg)
            self.pa_wg.close()
        self.adjustSize()

    def member_highest_level_chb_work(self):
        if self.member_highest_level_chb.isChecked():
            index = self.main_vbox.indexOf(self.member_highest_level_chb)
            self.main_vbox.insertWidget(index+1,self.mhl_wg)
            self.mhl_wg.adjustSize()
            self.mhl_wg.show()
        else:
            self.main_vbox.removeWidget(self.mhl_wg)
            self.mhl_wg.close()
        self.adjustSize()

    def guild_update_setting_chb_work(self):
        if self.guild_update_setting_chb.isChecked():
            index = self.main_vbox.indexOf(self.guild_update_setting_chb)
            self.main_vbox.insertWidget(index+1,self.gus_wg)
            self.gus_wg.adjustSize()
            self.gus_wg.show()
        else:
            self.main_vbox.removeWidget(self.gus_wg)
            self.gus_wg.close()
        self.adjustSize()

    def open_widget(self, widget_show):
        self.guilds_cb_work()
        DataManager.update_changes()
        widget_show()

    def refresh_guild_cb(self) -> None:
        self.guild_server_cb.clear()
        for s in DataManager.get_servers():
            self.guild_server_cb.addItem(s)

        self.guild_name_cb.clear()
        self.guild_name_cb.addItem("new")
        for g in DataManager.get_guilds(self.guild_server_cb.currentText()):
            self.guild_name_cb.addItem(g.name)

    def guilds_cb_work(self) -> None:
        current_guild_server= self.guild_server_cb.currentText()
        current_guild_name = self.guild_name_cb.currentText()
        DataManager.set_current_guild(server=current_guild_server, name=current_guild_name)

    def maple_account_chb_work(self) -> None:
        if self.maple_account_chb.isChecked():
            self.add_maple_account_box()
        else:
            self.del_maple_account_box()

    def add_maple_account_box(self) -> None:
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

    def del_maple_account_box(self) -> None:
        item = self.main_vbox.itemAt(5)
        widget = item.widget()
        self.main_vbox.removeWidget(widget)
        self.adjustSize()

    def add_guild(self) -> None:
        name = self.name_le.text()
        server = self.server_le.text()
        if server.isalpha():
            server = DataManager.server_eng_to_kor(server)
        position_count = self.position_count_sb.value()
        DataManager.add_guild(name=name, server=server, position_count=position_count)
        if self.maple_account_chb.isChecked():
            item = self.main_vbox.itemAt(5)
            widget: QGroupBox = item.widget()
            layout = widget.layout()
            id_item = layout.itemAt(0)
            id_layout = id_item.layout()
            id_le_item = id_layout.itemAt(1)
            id_widget: QLineEdit = id_le_item.widget()
            maple_id = id_widget.text()
            pw_item = layout.itemAt(1)
            pw_layout = pw_item.layout()
            pw_le_item = pw_layout.itemAt(1)
            pw_widget: QLineEdit = pw_le_item.widget()
            maple_pw = pw_widget.text()
            DataManager.set_guild_account(name=name, server=server, maple_id=maple_id,password=maple_pw)
        DataManager.update_changes()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = GuildAddWidget()
    wg.show()
    sys.exit(app.exec_())