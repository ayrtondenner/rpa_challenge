from writers.Writer import Writer
from helpers.debug_helper import print_debug_log
from helpers.constants import CSVConstants

import xlsxwriter

class XlsxWriter(Writer):
    def __init__(self, article_info_list):
        super().__init__(article_info_list)

    def __write_report_file__(self):

        try:
            workbook = xlsxwriter.Workbook(f"{self.__OUTPUT_FOLDER__}/nyt_report.xlsx")
            worksheet = workbook.add_worksheet()

            self.__write_xlsx_row__(worksheet, CSVConstants.CSV_HEADER, 0)

            for i, article_info in enumerate(self.article_info_list):
                row_data = []

                for header in CSVConstants.CSV_HEADER:
                    row_data.append(article_info[header])
                    self.__write_xlsx_row__(worksheet, row_data, i + 1)
            
            workbook.close()

        except Exception as ex:
            print_debug_log(f"Error when writing xlsx report: {ex}")

    def __write_xlsx_row__(self, worksheet, row_data, row):
        """Write a single xlsx row

        Args:
            worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object
            row_data (list): The row as a list of data
            row (int): The row index
        """
        col = 0

        for data in row_data:
            worksheet.write(row, col, data)

            col += 1