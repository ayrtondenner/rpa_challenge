from helpers import variables_helper
from helpers.debug_helper import print_debug_log

from writers.CSVWriter import CSVWriter
from crawlers.NYTCrawler import NYTCrawler

# Define a main() function that calls the other functions in order:
def main():
    print_debug_log("Task started")

    try:
        variables = variables_helper.get_work_variables()

        crawler = NYTCrawler()
        article_info_list = crawler.extract_data(variables)

        report_writer = CSVWriter(article_info_list)
        report_writer.write_report()
    except Exception as ex:
        print_debug_log(f"Error: {ex}")
    finally:
        print_debug_log("Task ended")


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
