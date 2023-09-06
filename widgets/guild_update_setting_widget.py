from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox
from PyQt5.QtCore import Qt
from data_manager import DataManager


class GuildUpdateSettingWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        DataManager.add_update_function(self.refresh)

        self.position_chb = QCheckBox("직위")
        self.job_chb = QCheckBox("직업")
        self.level_chb = QCheckBox("레벨")
        self.last_login_chb = QCheckBox("마지막 활동일")
        self.contribution_chb = QCheckBox("기여도")

        # self.position_chb.setLayoutDirection(Qt.RightToLeft)

        vbox = QVBoxLayout()
        vbox.addWidget(self.position_chb)
        vbox.addWidget(self.job_chb)
        vbox.addWidget(self.level_chb)
        vbox.addWidget(self.last_login_chb)
        vbox.addWidget(self.contribution_chb)

        self.setLayout(vbox)

    def initialize(self):
        self.position_chb.setChecked(False)
        self.job_chb.setChecked(False)
        self.level_chb.setChecked(False)
        self.last_login_chb.setChecked(False)
        self.contribution_chb.setChecked(False)

    def refresh(self):
        permissions = DataManager.get_current_permission()
        self.position_chb.setChecked(permissions["position"])
        self.job_chb.setChecked(permissions["job"])
        self.level_chb.setChecked(permissions["level"])
        self.last_login_chb.setChecked(permissions["last_login"])
        self.contribution_chb.setChecked(permissions["contribution"])

    def change_permission(self):
        position_state = self.position_chb.isChecked()
        job_state = self.job_chb.isChecked()
        level_state = self.level_chb.isChecked()
        last_login_state = self.last_login_chb.isChecked()
        contribution_state = self.contribution_chb.isChecked()
        DataManager.set_current_permission(
            position=position_state,
            job=job_state,
            level=level_state,
            last_login=last_login_state,
            contribution=contribution_state
        )

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    wg = GuildUpdateSettingWidget()
    wg.show()
    sys.exit(app.exec_())
