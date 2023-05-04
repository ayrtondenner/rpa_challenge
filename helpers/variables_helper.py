from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocorp.Vault import Vault
from helpers.debug_helper import print_debug_log

from helpers.constants import RPADefaultFilters, RPAFilterNames, URLs

def get_work_variables():
    """Read the filters variables to be used by the crawler

    Returns:
        dict: a dictionary with all needed variables
    """

    print_debug_log("Getting variables")

    website = URLs.WEBSITE
    website_query = URLs.WEBSITE_QUERY

    try:

        _secret = Vault().get_secret("credentials")

        USER_NAME = _secret["username"]
        PASSWORD = _secret["password"]

        work_items = WorkItems()
        work_items.get_input_work_item()

        try:
            search_phrase = work_items.get_work_item_variable(RPAFilterNames.SEARCH_PHRASE, RPADefaultFilters.SEARCH_PHRASE)
            if search_phrase == None: search_phrase = RPADefaultFilters.SEARCH_PHRASE
        except Exception as ex:
            print_debug_log(f"Loading default value for 'search_phrase': {ex}")
            search_phrase = RPADefaultFilters.SEARCH_PHRASE

        try:
            news_category_or_section = work_items.get_work_item_variable(RPAFilterNames.NEWS_CATEGORY_OR_SECTION, RPADefaultFilters.NEWS_CATEGORY_OR_SECTION)
            if not type(news_category_or_section) == list:
                news_category_or_section = RPADefaultFilters.NEWS_CATEGORY_OR_SECTION
        except Exception as ex:
            print_debug_log(f"Loading default value for 'news_section': {ex}")
            news_category_or_section = RPADefaultFilters.NEWS_CATEGORY_OR_SECTION

        try:
            months = work_items.get_work_item_variable(RPAFilterNames.MONTHS, RPADefaultFilters.MONTHS)
            if not type(months) == int or months < 0: months = RPADefaultFilters.MONTHS
        except Exception as ex:
            print_debug_log(f"Loading default value for 'months': {ex}")
            months = RPADefaultFilters.MONTHS

        print_debug_log("Input values loaded successfully.")

    except Exception as ex:
        print_debug_log(f"Error when loading variables: {ex}")
        print_debug_log("Loading default values")
        
        search_phrase = RPADefaultFilters.SEARCH_PHRASE
        news_category_or_section = RPADefaultFilters.NEWS_CATEGORY_OR_SECTION
        months = RPADefaultFilters.MONTHS

    finally:
        print_debug_log("Variables loaded")

        return {
            "website": website,
            "website_query": website_query,
            "search_phrase": search_phrase,
            "news_category_or_section": news_category_or_section,
            "months": months
        }