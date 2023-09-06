from PyQt5.QtWidgets import QApplication
from data_manager import DataManager
from widgets.main_widget import MyMainWindow
import sys

if __name__ == '__main__':
    DataManager.load()
    # DataManager.add_guild(name="봄날", server="오로라", position_count=7)
    app = QApplication(sys.argv)
    wg = MyMainWindow()
    wg.show()
    sys.exit(app.exec_())