from writers.Writer import Writer
from helpers.debug_helper import print_debug_log
from helpers.constants import CSVConstants

import csv

class CSVWriter(Writer):
    def __init__(self, article_info_list):
        super().__init__(article_info_list)

    def __write_report_file__(self):

        try:
            with open(f"{self.__OUTPUT_FOLDER__}/nyt_report.csv", "wt", encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=CSVConstants.CSV_FIELDNAMES)

                writer.writerow(CSVConstants.CSV_HEADER)

                writer.writerows(self.article_info_list)

        except Exception as ex:
            print_debug_log(f"Error when writing csv report: {ex}")