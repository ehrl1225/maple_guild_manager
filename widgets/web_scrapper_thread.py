from PyQt5.QtCore import QThread, pyqtSignal
from Guild import Guild
from WebScrapper import WebScrapper

class WebScrapperThread(QThread):
    done = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.guild:Guild = Guild("","")
        self.web_scrapper = WebScrapper()

    def run(self) -> None:
        self.web_scrapper.update_guild(guild=self.guild)
        self.done.emit()

    def set_guild(self, guild):
        self.guild = guild
