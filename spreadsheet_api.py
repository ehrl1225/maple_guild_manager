import gspread


class SpreadsheetManager:
    gc = gspread.service_account("service_account.json")

    def __init__(self):
        pass

    def open_by_url(self, url):
        self.sh = self.gc.open_by_url(url)
