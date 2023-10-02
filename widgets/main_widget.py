from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QComboBox, QCheckBox, QSpinBox, \
    QLabel, QTableWidgetItem, QPushButton, QMainWindow, QAction, QLineEdit
from widgets.my_table_widget import MyTableWidget
from widgets.guild_add_widget import GuildAddWidget
from data_manager import DataManager
from widgets.spreadsheet_widget import SpreadsheetWidget
from widgets.web_scrapper_thread import WebScrapperThread
import clipboard


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        DataManager.get_filtered_data_func = self.get_filtered_data_func
        self.initUI()

    def initUI(self):

        DataManager.add_update_function(self.update_data)
        self.properties: list[str] = [
            "이름",
            "직위",
            # "직업",
            "레벨",
            # "마지막 활동일",
            # "기여도",
            "표시"
        ]

        self.server_cb = QComboBox()
        self.guild_name_cb = QComboBox()
        self.update_btn = QPushButton("update")
        self.filter_group = QGroupBox()
        self.filter_group_layout = QVBoxLayout()
        self.filter_group.setLayout(self.filter_group_layout)
        self.filter_add_btn = QPushButton("add")
        self.filter_del_btn = QPushButton("del")
        self.filter_apply_btn = QPushButton("apply")
        self.copy_btn = QPushButton("copy")
        self.spliter_le = QLineEdit(":")

        self.tw = MyTableWidget()

        self.worker = WebScrapperThread()

        self.worker.done.connect(self.webcrawling_done)

        self.server_cb.currentIndexChanged.connect(self.guild_server_cb_work)

        self.update_btn.pressed.connect(self.refresh_data)

        self.filter_add_btn.pressed.connect(self.add_filter)
        self.filter_apply_btn.pressed.connect(self.apply_filter)
        self.copy_btn.pressed.connect(self.tw.copy)
        self.tw.copied.connect(self.copy_data)

        guild_hbox = QHBoxLayout()
        guild_hbox.addWidget(self.server_cb)
        guild_hbox.addWidget(self.guild_name_cb)

        copy_hbox = QHBoxLayout()
        copy_hbox.addWidget(self.spliter_le)
        copy_hbox.addWidget(self.copy_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(guild_hbox)
        vbox.addWidget(self.update_btn)
        vbox.addWidget(self.filter_add_btn)
        vbox.addWidget(self.filter_group)
        vbox.addWidget(self.filter_apply_btn)
        vbox.addWidget(self.tw)
        vbox.addLayout(copy_hbox)

        self.setLayout(vbox)

    def get_spliter(self):
        return self.spliter_le.text()

    @pyqtSlot(list)
    def copy_data(self, data: list[QTableWidgetItem]):
        pre_row = -1
        spliter = self.get_spliter()
        if spliter == "":
            spliter = ":"
        text = ""
        for d in data:
            if d.row() != pre_row:
                if pre_row != -1:
                    text += "\n"
                pre_row = d.row()
                text += d.text()
            else:
                text += spliter
                text += d.text()
        clipboard.copy(text)

    def refresh_data(self):
        guild_server = self.server_cb.currentText()
        guild_name = self.guild_name_cb.currentText()
        self.worker.set_guild(DataManager.get_guild(server=guild_server, name=guild_name))
        self.worker.start()
        self.update_btn.setDisabled(True)

    def webcrawling_done(self):
        self.update_btn.setEnabled(True)
        self.refresh_tb()

    def apply_filter(self):
        self.refresh_tb()

    def guild_server_cb_work(self):
        self.guild_name_cb.clear()
        if self.server_cb.currentIndex() != -1:
            server = self.server_cb.currentText()
            for g in DataManager.get_guilds(server):
                self.guild_name_cb.addItem(g.name)

    def update_data(self):
        self.server_cb.clear()
        self.server_cb.currentIndexChanged.disconnect(self.guild_server_cb_work)
        for s in DataManager.get_servers():
            self.server_cb.addItem(s)
        if self.server_cb.count() > 0:
            self.server_cb.setCurrentIndex(0)
        self.server_cb.currentIndexChanged.connect(self.guild_server_cb_work)
        self.guild_name_cb.clear()
        current_guild_server = self.server_cb.currentText()
        for g in DataManager.get_guilds(current_guild_server):
            self.guild_name_cb.addItem(g.name)

    def get_filtered_data_func(self):
        filters = self.get_filters()
        filtered_guild_members = DataManager.get_filtered_members(self.server_cb.currentText(),
                                                                  self.guild_name_cb.currentText(), filters[0])
        shows: set = set()
        del_shows: set = set()
        for f in filters[1]:
            name = f[1]
            contains = f[2]
            if contains:
                shows.add(name)
            else:
                del_shows.add(name)
        if len(shows) == 0:
            shows = set(self.properties[:-1])
        shows = shows - del_shows
        data = []
        for m_index, m in enumerate(filtered_guild_members):
            line = []
            if "이름" in shows:
                line.append(m.name)
            if "직위" in shows:
                kor_position = DataManager.position_eng_to_kor_alias(server=self.server_cb.currentText(),
                                                                     name=self.guild_name_cb.currentText(),
                                                                     eng_position=m.position)
                line.append(kor_position)
            if "직업" in shows:
                line.append(m.job)
            if "레벨" in shows:
                line.append(str(m.level))
            if "마지막 활동일" in shows:
                line.append(str(m.last_login))
            if "기여도" in shows:
                line.append(str(m.contribution))
            data.append(line)
        return data

    def refresh_tb(self):
        self.tw.clear()
        self.tw.setColumnCount(6)
        self.tw.setHorizontalHeaderLabels(self.properties)
        filters = self.get_filters()
        filtered_guild_members = DataManager.get_filtered_members(self.server_cb.currentText(),
                                                                  self.guild_name_cb.currentText(), filters[0])
        self.tw.setRowCount(len(filtered_guild_members))
        shows: set = set()
        del_shows: set = set()
        for f in filters[1]:
            name = f[1]
            contains = f[2]
            if contains:
                shows.add(name)
            else:
                del_shows.add(name)
        if len(shows) == 0:
            shows = set(self.properties[:-1])
        shows = shows - del_shows
        self.tw.setColumnCount(len(shows))
        shows_list = list()
        for p in self.properties:
            if p in shows:
                shows_list.append(p)
        self.tw.setHorizontalHeaderLabels(shows_list)
        for m_index, m in enumerate(filtered_guild_members):
            index = 0
            if "이름" in shows:
                name_item = QTableWidgetItem(m.name)
                self.tw.setItem(m_index, index, name_item)
                index += 1
            if "직위" in shows:
                kor_position = DataManager.position_eng_to_kor_alias(server=self.server_cb.currentText(),
                                                                     name=self.guild_name_cb.currentText(),
                                                                     eng_position=m.position)
                position_item = QTableWidgetItem(kor_position)
                self.tw.setItem(m_index, index, position_item)
                index += 1
            if "직업" in shows:
                job_item = QTableWidgetItem(m.job)
                self.tw.setItem(m_index, index, job_item)
                index += 1
            if "레벨" in shows:
                level_item = QTableWidgetItem(str(m.level))
                self.tw.setItem(m_index, index, level_item)
                index += 1
            if "마지막 활동일" in shows:
                last_login_item = QTableWidgetItem(str(m.last_login))
                self.tw.setItem(m_index, index, last_login_item)
                index += 1
            if "기여도" in shows:
                contribution_item = QTableWidgetItem(str(m.contribution))
                self.tw.setItem(m_index, index, contribution_item)
                index += 1


    def add_filter(self):
        group_box = QGroupBox()
        layout = QHBoxLayout()
        filters = self.properties[1:]
        filter_cb = QComboBox()
        del_btn = QPushButton("X")

        for f in filters:
            filter_cb.addItem(f)

        layout.addWidget(filter_cb)

        group_box.setLayout(layout)
        filter_cb.setCurrentIndex(0)

        def filter_cb_work():
            nonlocal layout
            for i in range(layout.count() - 1, 0, -1):
                item = layout.itemAt(i)
                wg = item.widget()
                layout.removeWidget(wg)
            item = layout.itemAt(0)
            cb: QComboBox = item.widget()
            current_text = cb.currentText()
            if current_text == "직위":
                position_cb = QComboBox()
                include_chb = QCheckBox("포함")

                for p in DataManager.get_position_names():
                    position_cb.addItem(p)

                layout.addWidget(position_cb)
                layout.addWidget(include_chb)

            elif current_text == "직업":
                job_cb = QComboBox()
                include_chb = QCheckBox("포함")

                for j in DataManager.get_jobs(self.server_cb.currentText(), self.guild_name_cb.currentText()):
                    job_cb.addItem(j)
                layout.addWidget(job_cb)
                layout.addWidget(include_chb)

            elif current_text == "레벨":
                min_level = QSpinBox()
                wave_lb = QLabel("~")
                max_level = QSpinBox()
                layout.addWidget(min_level)
                layout.addWidget(wave_lb)
                layout.addWidget(max_level)

            elif current_text == "마지막 활동일":
                min_date = QSpinBox()
                wave_lb = QLabel("~")
                max_date = QSpinBox()
                layout.addWidget(min_date)
                layout.addWidget(wave_lb)
                layout.addWidget(max_date)

            elif current_text == "기여도":
                min_date = QSpinBox()
                wave_lb = QLabel("~")
                max_date = QSpinBox()
                layout.addWidget(min_date)
                layout.addWidget(wave_lb)
                layout.addWidget(max_date)

            elif current_text == "표시":
                item_cb = QComboBox()
                shows_chb = QCheckBox("보임")
                shows_chb.setChecked(True)
                for i in self.properties[:-1]:
                    item_cb.addItem(i)
                layout.addWidget(item_cb)
                layout.addWidget(shows_chb)

            else:
                pass
            layout.addWidget(del_btn)
            del_btn.pressed.connect(partial(self.filter_group_layout.removeWidget, group_box))

        filter_cb_work()

        filter_cb.currentIndexChanged.connect(filter_cb_work)
        self.filter_group_layout.addWidget(group_box)

    def get_filters(self):
        member_filters = []
        show_filters = []
        filter_counter = self.filter_group_layout.count()
        for i in range(filter_counter):
            item = self.filter_group_layout.itemAt(i)
            group_box: QGroupBox = item.widget()
            group_box_layout: QHBoxLayout = group_box.layout()
            cb_item = group_box_layout.itemAt(0)
            cb: QComboBox = cb_item.widget()
            cb_text = cb.currentText()

            if cb_text in ["직위", "직업"]:
                date_cb: QComboBox = group_box_layout.itemAt(1).widget()
                data = date_cb.currentText()
                includes_chb: QCheckBox = group_box_layout.itemAt(2).widget()
                includes = includes_chb.isChecked()
                filter = [cb_text, data, includes]
                member_filters.append(filter)

            elif cb_text in ["레벨", "마지막 활동일", "기여도"]:
                min_sp: QSpinBox = group_box_layout.itemAt(1).widget()
                min_value = min_sp.value()
                max_sp: QSpinBox = group_box_layout.itemAt(2).widget()
                max_value = max_sp.value()
                filter = [cb_text, min_value, max_value]
                member_filters.append(filter)
            elif cb_text == "표시":
                date_cb: QComboBox = group_box_layout.itemAt(1).widget()
                data = date_cb.currentText()
                show_chb: QCheckBox = group_box_layout.itemAt(2).widget()
                shows = show_chb.isChecked()
                filter = [cb_text, data, shows]
                show_filters.append(filter)
        return [member_filters, show_filters]


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.my_wg = MainWidget()
        self.guild_setting_wg = GuildAddWidget()
        self.spreadsheet_wg = SpreadsheetWidget()
        self.initUI()

    def initUI(self):
        self.setting = QAction("길드 설정", self)
        self.setting.triggered.connect(self.guild_setting_wg.show)

        self.spreadsheet = QAction("스프레드시트", self)
        self.spreadsheet.triggered.connect(self.spreadsheet_wg.show)

        self.save = QAction("저장", self)
        self.save.setShortcut(QKeySequence("Ctrl+S"))
        self.save.triggered.connect(self.save_data)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        settingMenu = menubar.addMenu("&설정")
        settingMenu.addAction(self.setting)
        settingMenu.addAction(self.spreadsheet)
        settingMenu.addAction(self.save)

        self.setCentralWidget(self.my_wg)

    def save_data(self):
        DataManager.save()

    def refresh(self):
        self.my_wg.update_data()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    wg = MyMainWindow()
    wg.show()
    sys.exit(app.exec_())
