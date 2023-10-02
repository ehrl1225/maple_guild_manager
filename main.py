from PyQt5.QtWidgets import QApplication
from data_manager import DataManager
from widgets.main_widget import MyMainWindow
import sys

if __name__ == '__main__':

    DataManager.load()

    app = QApplication(sys.argv)
    wg = MyMainWindow()

    wg.show()
    wg.refresh()
    sys.exit(app.exec_())