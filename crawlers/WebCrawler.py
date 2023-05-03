from RPA.Browser.Selenium import Selenium
from helpers.debug_helper import print_debug_log

class WebCrawler:
    def __init__(self):
        self.__browser__ = Selenium()

    def extract_data(self):
        """Method that must be implemented in child class

        Raises:
            NotImplementedError: this method must be implemented in child class
        """
        raise NotImplementedError("Calling generic extract_data method")
    
    def __open_browser_in_website__(self, url):
        """Start a new browser instance and open it in the url

        Args:
            url (str): The website url
        """
        print_debug_log(f"Opening browser in url: {url}")

        #self.__browser__.open_headless_chrome_browser(url)
        self.__browser__.open_available_browser(url)

        self.__browser__.maximize_browser_window()
        print_debug_log("Website open")

    def __close_browser__(self):
        """Close the browser instance
        """
        print_debug_log("Closing browser")
        self.__browser__.close_all_browsers()

    def __get_attribute_inner_html__(self, element_path):
        """Get attribute "innerHTML" from Selenium element

        Args:
            element_path (str): element xpath

        Returns:
            str: The "innerHTML" attribute from element
        """
        try:
            return self.__browser__.find_element(element_path).get_attribute("innerHTML")
        except Exception as ex:
            print_debug_log(f"Error when getting inner html attribute: {ex}")
            return None
        
    def __get_element_count__(self, xpath):
        """Get element count in browser

        Args:
            xpath (str): xpath from one or more elements

        Returns:
            int: element count that matches the xpath
        """
        element_count = 0

        try:
            element_count = self.__browser__.get_element_count(xpath)
        except Exception as ex:
            print_debug_log(f"Error when getting element count: {ex}")
        finally:
            return element_count