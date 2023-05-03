from RPA.Browser.Selenium import Selenium
from helpers.debug_helper import print_debug_log

class WebCrawler:
    def __init__(self):
        self.__browser__ = Selenium()

    def extract_data(self):
        raise NotImplementedError("Calling generic extract_data method")
    
    def __open_browser_in_website__(self, url):
        print_debug_log(f"Opening browser in url: {url}")

        #self.__browser__.open_headless_chrome_browser(url)
        self.__browser__.open_available_browser(url)

        self.__browser__.maximize_browser_window()
        print_debug_log("Website open")

    def __close_browser__(self):
        print_debug_log("Closing browser")
        self.__browser__.close_all_browsers()

    def __get_attribute_inner_html__(self, element_path):
        try:
            return self.__browser__.find_element(element_path).get_attribute("innerHTML")
        except Exception as ex:
            print_debug_log(f"Error when getting inner html attribute: {ex}")
            return None
        
    def __get_element_count__(self, xpath):
        element_count = 0

        try:
            element_count = self.__browser__.get_element_count(xpath)
        except Exception as ex:
            print_debug_log(f"Error when getting element count: {ex}")
        finally:
            return element_count