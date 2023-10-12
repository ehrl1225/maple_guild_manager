try:
    from PyQt5.QtWidgets import QApplication
    from data_manager import DataManager
    from widgets.main_widget import MyMainWindow
    import sys
except ModuleNotFoundError:
    import os
    try:
        os.system("python3 -m pip install bs4")
    except ModuleNotFoundError:
        if os.name == "posix":
            os.system("sudo apt install python3-pip")
            os.system("python3 -m pip install bs4")
    os.system("python3 -m pip install selenium")
    os.system("python3 -m pip install chromedriver_autoinstaller")
    os.system("python3 -m pip install pyqt5")
    os.system("python3 -m pip install clipboard")
    os.system("python3 -m pip install gspread")
    os.system("python3 -m pip install xlsxwriter")
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
