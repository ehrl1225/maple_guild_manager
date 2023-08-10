from PyQt5.QtCore import QThread
from Guild import Guild
from WebScrapper import WebScrapper

class WebScrapperThread(QThread):

    def __init__(self):
        super().__init__()
        self.guild:Guild = Guild("","")
        self.web_scrapper = WebScrapper()

    def run(self) -> None:
        pass
