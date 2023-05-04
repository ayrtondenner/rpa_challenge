from RPA.Browser.Selenium import Selenium
from helpers.debug_helper import print_debug_log
from helpers import date_helper

class WebCrawler:
    def __init__(self):
        self.__browser__ = Selenium()

    def extract_data(self):
        """Method that must be implemented in child class

        Raises:
            NotImplementedError: this method must be implemented in child class
        """
        raise NotImplementedError("Calling generic extract_data method")
    
    def __print_variable_dictionary__(self, variables_dict):
        """Print all relevant variables used in robot crawler

        Args:
            variables_dict (dict): the variables dictionary
        """
        website = variables_dict['website']
        search_query = variables_dict['search_phrase']
        news_section = variables_dict['news_category_or_section']
        months = variables_dict['months']

        print_debug_log(f"Website: '{website}'")
        print_debug_log(f"Search query: '{search_query}'")
        print_debug_log(f"News section: {news_section}")
        print_debug_log(f"Months: {months}")

    def __calculate_start_and_end_date_strings__(self, months):
        """Calculates start and end date strings

        Args:
            months (int): the months int filter

        Returns:
            str, str: the start and end date as strings
        """

        # Fixing months value
        months = date_helper.fixing_months_variable(months)
        start_date_string, end_date_string = date_helper.calculate_start_and_end_date(months)

        return start_date_string, end_date_string
    
    def __open_browser_in_website__(self, url):
        """Start a new browser instance and open it in the url

        Args:
            url (str): The website url
        """
        print_debug_log(f"Opening browser in url: {url}")

        self.__browser__.open_headless_chrome_browser(url)
        #self.__browser__.open_available_browser(url)

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