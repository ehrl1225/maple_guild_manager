import time

from PyQt5.QtCore import QThread

class SpreadsheetThread(QThread):

    def __init__(self):
        super().__init__()
        self.go = True
        self.queue = []

    def run(self) -> None:
        while self.go:
            if self.queue:
                p = self.queue.pop(0)
                p()
            time.sleep(1)
