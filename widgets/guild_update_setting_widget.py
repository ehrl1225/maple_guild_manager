from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from data_manager import DataManager


class GuildUpdateSettingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        DataManager.add_update_function(self.refresh)

        self.position_chb = QCheckBox()
        self.job_chb = QCheckBox()
        self.level_chb = QCheckBox()
        self.last_login_chb = QCheckBox()
        self.contribution_chb = QCheckBox()

        vbox = QVBoxLayout()
        vbox.addWidget(self.position_chb)
        vbox.addWidget(self.job_chb)
        vbox.addWidget(self.level_chb)
        vbox.addWidget(self.last_login_chb)
        vbox.addWidget(self.contribution_chb)

        self.setLayout(vbox)

    def refresh(self):
        pass

    def change_permission(self):
        current_guild = DataManager.get_current_guild()
        position_state = self.position_chb.isChecked()
        job_state = self.job_chb.isChecked()
        level_state = self.level_chb.isChecked()
        last_login_state = self.last_login_chb.isChecked()
        contribution_state = self.contribution_chb.isChecked()
        current_guild.set_permissions(
            position=position_state,
            job=job_state,
            level=level_state,
            last_login=last_login_state,
            contribution=contribution_state
        )
