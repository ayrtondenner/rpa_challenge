from crawlers.WebCrawler import WebCrawler

from SeleniumLibrary.errors import ElementNotFound

from helpers import date_helper
from helpers.debug_helper import print_debug_log

import re, time
from helpers.constants import Regexes, OtherConstants, XPaths

class NYTCrawler(WebCrawler):
    def __init__(self):
        super().__init__()

    def extract_data(self, variables_dict):
        """Extract data from website

        Args:
            variables_dict (dict): Variables dictionary

        Returns:
            list: list of article dicts
        """
        self.variables_dict = variables_dict

        article_info_list = []

        print_debug_log("Starting crawler")

        try:

            self.__print_variable_dictionary__(self.variables_dict)
            start_date_string, end_date_string = self.__calculate_start_and_end_date_strings__(self.variables_dict["months"])

            self.__open_browser_in_website__(self.variables_dict["website"])

            self.__access_search_page__(self.variables_dict["search_phrase"], self.variables_dict["website_query"])
            self.__close_cookies_window__()
            self.__apply_date_range_filter__(start_date_string, end_date_string)
            self.__apply_section_filter__(self.variables_dict["news_category_or_section"])
            self.__select_sort_by_newest__()
            self.__press_search_page_button__()
            article_info_list = self.__extract_articles__(self.variables_dict["search_phrase"])

        except Exception as ex:
            print_debug_log(f"Error when scrapping the website: {ex}")
        finally:
            self.__close_browser__()
            print_debug_log("Crawler work is done!")

            return article_info_list

    # The test says to navigate to website, fill a term in the search field, and click it
    # That's why I followed these steps
    # But in real life, I would probably do a direct access to search URL. Example:
    # self.__browser__.go_to(https://www.nytimes.com/search?query=economy&sections=Opinion%7Cnyt%3A%2F%2Fsection%2Fd7a71185-aa60-5635-bce0-5fab76c7c297&sort=newest&startDate=20230401&endDate=20230502)
    def __access_search_page__(self, query, website_query):
        """Access search page

        Args:
            query (str): the query search
            website_query (str): the URL for the direct search page
        """
        print_debug_log("Accessing search page")
        try:
            self.__browser__.click_button(XPaths.MAIN_PAGE_SEARCH_BUTTON)
            self.__browser__.input_text(XPaths.MAIN_PAGE_SEARCH_INPUT, query)
            self.__browser__.click_button(XPaths.MAIN_PAGE_SEARCH_SUBMIT)
        except Exception as ex:
            # If something wrong happens, let's go straight to the search page

            print_debug_log(f"Error when accessing the search page: {ex}")
            print_debug_log("Accessing search page via direct URL")

            website_query_url = website_query.format(query = query)
            self.__browser__.go_to(website_query_url)
        print_debug_log("Search page accessed")

    def __close_cookies_window__(self):
        """Close the cookies window
        """
        print_debug_log("Closing cookies window")
        try:
            self.__browser__.click_button(XPaths.COOKIE_WINDOW_CLOSE_BUTTON)
        except Exception as ex:
            print_debug_log(f"Error when closing cookies window: {ex}")

    def __apply_date_range_filter__(self, start_date_string, end_date_string):
        """Apply the date range filter

        Args:
            start_date_string (str): The start date
            end_date_string (str): The end date
        """
        try:
            print_debug_log("Applying date filter")

            date_range_selector = self.__browser__.find_element(XPaths.SEARCH_PAGE_DATE_DROPDOWN)
            date_range_selector.click()
            
            # Unfortunately there's no id for this button or any parent element
            # So we had to go after child button via "value" property
            self.__browser__.click_button(XPaths.SEARCH_PAGE_SPECIFIC_DATES)
            
            self.__browser__.input_text("startDate", start_date_string)
            self.__browser__.input_text("endDate", end_date_string)

        except Exception as ex:
            print_debug_log(f"Error when applying date range filter: {ex}")
        finally:
            if "popup-visible" in date_range_selector.get_attribute("class"):
                # Clicking again to dismiss the dialog
                date_range_selector.click()

        print_debug_log("Date filter done")

    def __apply_section_filter__(self, news_category_list):
        """Apply the section filter

        Args:
            news_category_list (list): the list of news categories filters
        """
        print_debug_log("Applying sections filter")

        try:
            # If there's no category to select, we can let the filter as it is
            # Which is the "Any" category
            if len(news_category_list) == 0:
                print_debug_log("No section filter to select")
                return

            section_selector = self.__browser__.find_element(XPaths.SEARCH_PAGE_SECTION_DROPDOWN)
            section_selector.click()

            for news_category in news_category_list:
                try:
                    news_category_xpath = XPaths.SEARCH_PAGE_SECTION_SELECTOR.format(news_category = news_category)

                    section_search_count = self.__get_element_count__(news_category_xpath)

                    if section_search_count == 1:
                        self.__browser__.click_element(news_category_xpath)
                    else:
                        print_debug_log(f"Section '{news_category}' not found")
                except Exception as ex:
                    print_debug_log(f"Error when trying to select '{news_category}' filter section: {ex}")

        except Exception as ex:
            print_debug_log(f"Error when applying section filter: {ex}")
            print_debug_log(f"Reselecting 'any' section")

            # If any major error happens
            # we will go back to selecting "Any" section
            self.__select_section_any__()
        finally:
            # Clicking again to dismiss the dialog
            if "popup-visible" in section_selector.get_attribute("class"):
                section_selector.click()

        print_debug_log("Section filter done")


    def __select_section_any__(self):
        """Select the "any" option in the section filter
        """
        try:
            section_button = self.__browser__.find_element(XPaths.SEARCH_PAGE_SECTION_DROPDOWN)

            section_button_class = section_button.get_attribute("class")

            # This means that the Section dialog is not open
            if not "popup-visible" in section_button_class:
                section_button.click()

            self.__browser__.click_element(XPaths.SEARCH_PAGE_SECTION_ANY_SELECTOR)

        except Exception as ex:
            print_debug_log(f"Error when applying 'Any' section filter: {ex}")
        finally:
            # Clicking again to dismiss the dialog
            if "popup-visible" in section_button.get_attribute("class"):
                section_button.click() 

    def __select_sort_by_newest__(self):
        """Select the "sort by newest" option in the search page
        """
        print_debug_log("Sorting by newest")

        try:
            sort_selector = self.__browser__.find_element(XPaths.SEARCH_PAGE_SORT_BY_SELECTOR)

            sort_selector.click()
            self.__browser__.click_element(XPaths.SEARCH_PAGE_SORT_BY_NEWEST)
        except Exception as ex:
            print_debug_log(f"Error when sorting by newest: {ex}")
        finally:
            # Clicking again to dismiss the dialog
            sort_selector.click()

    # In best case scenario, we do not need to press this button
    # since the sort update will already update the query result
    # But if anything wrong happens, this click will ensure that the search will happen anyway
    def __press_search_page_button__(self):
        """Press the "search" button
        """
        print_debug_log("Pressing search button")
        try:
            self.__browser__.click_button(XPaths.SEARCH_PAGE_SEARCH_BUTTON)
            print_debug_log("Search button pressed")
        except Exception as ex:
            print_debug_log(f"Error when pressing the search button: {ex}")

    def __extract_articles__(self, query):
        """Scrolls through all query results and extract all articles info

        Args:
            query (str): the search query

        Returns:
            list: the list of articles dict info
        """
        article_info_list = []

        # Let's wait for the page results to load before extracting all articles
        time.sleep(5)

        try:
            article_info_list = self.__scroll_all_articles__(query)
        except Exception as ex:
            print_debug_log(f"Error when extracting articles info: {ex}")
        finally:
            return article_info_list

    def __scroll_all_articles__(self, query):
        """Scroll all articles in search page

        Args:
            query (str): the search query

        Returns:
            list: the list of articles info dict
        """

        print_debug_log("Scrolling articles list")
        article_info_list = []

        results_count = 0

        # Reading the results count from search page
        try:
            results_label = self.__browser__.find_element(XPaths.SEARCH_PAGE_RESULT_LABEL)
            results_match = re.match(Regexes.SEARCH_PAGE_LABEL_REGEX, results_label.text)

            if results_match:
                results_count = int(results_match.group(1))

        except Exception as ex:
            print_debug_log(f"Error when reading search results label: {ex}")

        keep_clicking_show_more_button = True

        articles_count = self.__get_element_count__(XPaths.ARTICLES_LIST)

        # Today, NYTimes is only loading in batches of 10 articles
        # But if this changes in the future, it won't affect our bot
        articles_to_read_count = articles_count - len(article_info_list)
        article_info_sublist = self.__get_articles_info__(query, articles_to_read_count, results_count)
        article_info_list.extend(article_info_sublist)
        
        while self.__get_element_count__(XPaths.SEARCH_PAGE_SHOW_MORE_BUTTON) == 1 and keep_clicking_show_more_button:
            try:
                keep_clicking_show_more_button = self.__click_in_show_more_button_and_load_more_data__()
                articles_count = self.__get_element_count__(XPaths.ARTICLES_LIST)

                # Reading the new loaded articles
                articles_to_read_count = articles_count - len(article_info_list)
                article_info_sublist = self.__get_articles_info__(query, articles_to_read_count, results_count)
                article_info_list.extend(article_info_sublist)

            # Sometimes, when clicking the last instance of "show more" button, the following situation appears
            # The bot checks that the button still exists, then NYT website destroys the button, and then the bot will try to click the button that previously existed
            # Because Selenium is faster than the destruction of the button, it's important to check any issue related when trying to click it
            except ElementNotFound as ex:
                if XPaths.SEARCH_PAGE_SHOW_MORE_BUTTON in str(ex):
                    print_debug_log("Stopped after no more instances of \"show more\" button")
                else:
                    print_debug_log(f"Stopped after unexpected \"ElementNotFound\" error: {ex}")

                break
            except Exception as ex:
                print_debug_log(f"Stopped after unexpected \"Exception\" error: {ex}")

        # Scrolling to page bottom
        self.__browser__.execute_javascript(XPaths.SCROLL_TO_PAGE_BOTTOM)

        articles_count = self.__get_element_count__(XPaths.ARTICLES_LIST)
        print_debug_log(f"Total scrolling of {articles_count} articles")

        return article_info_list


    def __click_in_show_more_button_and_load_more_data__(self):
        """Click in the "show more" button and load more data
        This function will finish only after being sure that more data was actually loaded

        Returns:
            bool: returns a variable to show if the bot should keeps trying to click in the button
        """
        articles_count = self.__get_element_count__(XPaths.ARTICLES_LIST)

        click_tries = 0
        keep_clicking_show_more_button = True

        while True:
            try:

                self.__browser__.scroll_element_into_view(XPaths.SEARCH_PAGE_SHOW_MORE_BUTTON)
                self.__browser__.click_button_when_visible(XPaths.SEARCH_PAGE_SHOW_MORE_BUTTON)

                # Let's wait for the page to load more articles
                await_condition = XPaths.SEARCH_PAGE_LOAD_ARTICLES_AWAIT_CONDITION.format(articles_count = articles_count)
                self.__browser__.wait_for_condition(await_condition, 10)

                # Wait a few seconds to avoid conflict when clicking the button again
                time.sleep(2)

                break
            
            except AssertionError as ex:
                click_tries += 1

                if click_tries < OtherConstants.MAX_TRIES_IN_SHOW_MORE_BUTTON:
                    # Sometimes we click but the articles do not load
                    # Console shows it's a inner problem in the GraphQL in NYTimes
                    # It's better to try to click it again
                    print_debug_log("AssertionError when clicking \"show more\" button, let's click it again")
                    continue
                else:
                    # After trying a few times, the button won't work anymore
                    print_debug_log(f"We already tried {click_tries} times. The button is not going to work anymore")
                    keep_clicking_show_more_button = False
                    break
            except Exception as ex:
                print_debug_log(f"Exception when clicking \"show more\" button: {ex}")
                break

        return keep_clicking_show_more_button
            

    def __get_articles_info__(self, query, articles_to_read_count, results_count):
        """Get info from all visible articles

        Args:
            query (str): the search query
            articles_to_read_count (int): count of last n articles to read
            results_count (int): total count of articles

        Returns:
            list: the list of visible articles info dict
        """
        article_info_list = []

        articles_count = self.__get_element_count__(XPaths.ARTICLES_LIST)

        query_lower = query.lower()

        # Selenium selector starts from 1
        for i in range(articles_count - articles_to_read_count + 1, articles_count + 1):
            try:

                
                picture_xpath = XPaths.ARTICLE_PICTURE.format(i = i)

                title = self.__get_attribute_inner_html__        (XPaths.ARTICLE_TITLE.format(i = i))
                date = self.__get_attribute_inner_html__         (XPaths.ARTICLE_DATE.format(i = i))
                description = self.__get_attribute_inner_html__  (XPaths.ARTICLE_DESCRIPTION.format(i = i))
                picture_url = None            

                # Some articles do not have image
                if len(self.__browser__.find_elements(picture_xpath)) > 0:
                    picture_url = self.__browser__.find_element(picture_xpath).get_attribute("src")
                    picture_url = self.__remove_params_from_url_string__(picture_url)
                
                date = date_helper.convert_hours_ago_label_to_today_date(date)
                title_lower = title.lower()
                description_lower = description.lower()

                search_phrases_count = title_lower.count(query_lower) + description_lower.count(query_lower)
                contains_money = (
                    len(re.findall(Regexes.CURRENCY_REGEX_LIST_JOINED, title_lower)) > 0
                    or
                    len(re.findall(Regexes.CURRENCY_REGEX_LIST_JOINED, description_lower)) > 0
                )

                article_dict = {
                    "title": title,
                    "date": date,
                    "description": description,
                    "picture_url": picture_url,
                    "search_phrases_count": search_phrases_count,
                    "contains_money": contains_money
                }

                article_info_list.append(article_dict)

            except Exception as ex:
                print_debug_log(f"Exception when trying to extract info from article #{i}: {ex}")


        if results_count > 0:
            scroll_percentage = round(articles_count / results_count * 100)
            print_debug_log(f"Scrolled through {articles_count}/{results_count} ({scroll_percentage}%) articles")
        else:
            print_debug_log(f"Scrolled through {articles_count} articles")
        
        return article_info_list