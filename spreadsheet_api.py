import gspread
from gspread.utils import column_letter_to_index, rowcol_to_a1
from xlsxwriter.utility import xl_col_to_name


class SpreadsheetManager:
    # print(os.getcwd())
    gc = gspread.service_account("data/service_account.json")
    sh: gspread.Spreadsheet
    worksheet: gspread.worksheet
    all_value: list[list[str]]

    def __init__(self):
        pass

    def open_by_url(self, url) -> int:
        try:
            self.sh = self.gc.open_by_url(url)
            return 0
        except gspread.exceptions.APIError:
            return -1

    def get_titles(self):
        titles = []
        for worksheet in self.sh.worksheets():
            titles.append(worksheet.title)
        return titles

    def get_worksheet(self, title):
        for worksheet in self.sh.worksheets():
            if worksheet.title == title:
                self.worksheet = worksheet
                break

    def get_col_to_num(self, col_str):
        try:
            num = column_letter_to_index(col_str)
            return num
        except gspread.exceptions.InvalidInputValue:
            return -1

    def get_horizontal_headers(self, col):
        data = []
        for i in range(col, col + 10):
            i -= 1
            if i == -1:
                data.append("X")
            else:
                data.append(xl_col_to_name(i))
        return data

    def get_vertical_header(self, row):
        data = []
        for i in range(row, row + 10):
            if i == 0:
                data.append("X")
            else:
                data.append(str(i))
        return data

    def update_data(self, row, col, data: list[list[object]]):
        row_count = len(data)
        col_count = len(data[0])
        from_str = rowcol_to_a1(row, col)
        to_str = rowcol_to_a1(row + row_count, col + col_count)
        self.worksheet.update(f"{from_str}:{to_str}", data)

    def get_data(self, row, col):
        self.all_data = self.worksheet.get_all_values()
        data = [["" for __ in range(10)] for _ in range(10)]
        row -= 2
        col -= 2
        all_data_row = len(self.all_data)
        all_data_col = len(self.all_data[0])
        row_end = min(row + 10, all_data_row)
        col_end = min(col + 10, all_data_col)
        for row_index, i in enumerate(range(row, row_end)):
            if i < 0:
                continue
            for col_index, j in enumerate(range(col, col_end)):
                if j < 0:
                    continue
                data[row_index][col_index] = self.all_data[i][j]
        return data


if __name__ == '__main__':

    pass
