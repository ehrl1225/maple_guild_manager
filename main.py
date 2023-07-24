from PyQt5.QtWidgets import QApplication
from data_manager import DataManager
import sys

if __name__ == '__main__':
    DataManager.load()
    app = QApplication(sys.argv)
    # put widget here
    sys.exit(app.exec_())