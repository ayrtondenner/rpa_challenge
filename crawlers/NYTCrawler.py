from crawlers.WebCrawler import WebCrawler

from SeleniumLibrary.errors import ElementNotFound

from helpers import date_helper
from helpers.debug_helper import print_debug_log

import re
from helpers.constants import Regexes, OtherConstants

class NYTCrawler(WebCrawler):
    def __init__(self):
        super().__init__()

    def extract_data(self, variables_dict):
        self.variables_dict = variables_dict

        article_info_list = []

        print_debug_log("Starting crawler")

        try:

            self.__open_browser_in_website__(self.variables_dict["website"])

            self.__access_search_page__(self.variables_dict["search_phrase"], self.variables_dict["website_query"])
            self.__close_cookies_windows__()
            self.__apply_date_range_filter__(self.variables_dict["months"])
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
    # That's why I've done this way
    # But in real life, I would probably do a direct access to search URL. Example:
    # self.__browser__.go_to(https://www.nytimes.com/search?query=economy&sections=Opinion%7Cnyt%3A%2F%2Fsection%2Fd7a71185-aa60-5635-bce0-5fab76c7c297&sort=newest&startDate=20230401&endDate=20230502)
    def __access_search_page__(self, query, website_query):
        print_debug_log("Accessing search page")
        try:
            self.__browser__.click_button("xpath://button[@data-test-id='search-button']")
            self.__browser__.input_text("xpath://input[@data-testid='search-input']", query)
            self.__browser__.click_button("xpath://button[@data-test-id='search-submit']")
        except Exception as ex:
            # If something wrong happens, let's go straight to the search page

            print_debug_log(f"Error when accessing the search page: {ex}")
            print_debug_log("Accessing search page via direct URL")

            website_query_url = website_query.format(query = query)
            self.__browser__.go_to(website_query_url)
        print_debug_log("Search page accessed")

    def __close_cookies_windows__(self):
        print_debug_log("Closing cookies window")
        try:
            self.__browser__.click_button("xpath://button[@data-testid='expanded-dock-btn-selector']")
        except Exception as ex:
            print_debug_log(f"Error when closing cookies window: {ex}")


    def __apply_date_range_filter__(self, months):
        try:
            print_debug_log("Applying date filter")

            # Fixing months if something happens
            months = date_helper.fixing_months_variable(months)
            start_date_string, end_date_string = date_helper.calculate_start_and_end_date(months)

            date_range_selector = self.__browser__.find_element("xpath://button[@data-testid='search-date-dropdown-a']")
            date_range_selector.click()
            
            # Unfortunately there's no id for this button or any parent element
            # So we had to go after child button via "value" property
            self.__browser__.click_button("xpath://div[@aria-label='Date Range']//button[@value='Specific Dates']")
            
            self.__browser__.input_text("startDate", start_date_string)
            self.__browser__.input_text("endDate", end_date_string)

            # Clicking again to dismiss the dialog
            date_range_selector.click()
        except Exception as ex:
            print_debug_log(f"Error when applying date range filter: {ex}")

        print_debug_log("Date filter done")

    def __apply_section_filter__(self, news_category_list):
        print_debug_log("Applying sections filter")

        try:
            # If there's no category to select, we can let the filter as it is
            # Which is the "Any" category
            if len(news_category_list) == 0:
                pass

            section_selector = self.__browser__.find_element("xpath://button[@data-testid='search-multiselect-button']")
            section_selector.click()

            for news_category in news_category_list:
                try:
                    section_search_count = self.__get_element_count__(f"//span[text()='{news_category}']")

                    if section_search_count == 1:
                        self.__browser__.click_element(f"//span[text()='{news_category}']")
                    else:
                        print_debug_log(f"Section '{news_category}' not found")
                except Exception as ex:
                    print_debug_log(f"Error when trying to select '{news_category}' filter section: {ex}")

            # Clicking again to dismiss the dialog
            section_selector.click()
        except Exception as ex:
            print_debug_log(f"Error when applying section filter: {ex}")
            print_debug_log(f"Reselecting 'any' section")

            # If any major error happens
            # we will go back to selecting "Any" section
            self.__select_section_any__()

        print_debug_log("Section filter done")


    def __select_section_any__(self):
        try:
            section_button = self.__browser__.find_element(f"xpath://button[@data-testid='search-multiselect-button']")

            section_button_class = section_button.get_attribute("class")

            # This means that the Section dialog is not open
            if not "popup-visible" in section_button_class:
                section_button.click()

            self.__browser__.click_element(f"//span[text()='Any']")

            # Clicking again to dismiss the dialog
            section_button.click()

        except Exception as ex:
            print_debug_log(f"Error when applying 'Any' section filter: {ex}")

    def __select_sort_by_newest__(self):
        print_debug_log("Sorting by newest")

        try:
            sort_selector = self.__browser__.find_element("xpath://select[@data-testid='SearchForm-sortBy']")

            sort_selector.click()
            self.__browser__.click_element("xpath://select[@data-testid='SearchForm-sortBy']/option[@value='newest']")
            
            # Clicking again to dismiss the dialog
            sort_selector.click()
            print_debug_log("Selected sort by newest")
        except Exception as ex:
            print_debug_log(f"Error when sorting by newest: {ex}")

    # In best case scenario, isn't needed to press this button
    # since the sort update will already update the query result
    # But if anything wrong happens, this click will ensure that the search will happen anyway
    def __press_search_page_button__(self):
        print_debug_log("Pressing search button")
        try:
            self.__browser__.click_button("xpath://button[@data-testid='search-page-submit']")
            print_debug_log("Search button pressed")
        except Exception as ex:
            print_debug_log(f"Error when pressing the search button: {ex}")

    def __extract_articles__(self, query):
        article_info_list = []

        try:
            self.__scroll_all_articles__()
            article_info_list = self.__get_articles_info__(query)
        except Exception as ex:
            print_debug_log(f"Error when extracting articles info: {ex}")
        finally:
            return article_info_list

    def __scroll_all_articles__(self):
        print_debug_log("Scrolling articles list")

        show_more_button_xpath = "xpath://button[@data-testid='search-show-more-button']"
        articles_xpath = "xpath://ol[@data-testid='search-results']//li[@data-testid='search-bodega-result']"

        keep_trying = True
        
        while self.__get_element_count__(show_more_button_xpath) == 1 and keep_trying:
            try:
                keep_trying = self.__click_in_show_more_button__(show_more_button_xpath, articles_xpath)

            # Sometimes, when clicking the last instance of "show more" button, the following situation appears
            # The bot checks that the button still exists, then NYT website destroys the button, and then the bot will try to click the button that previously existed
            # Because Selenium is faster than the destruction of the button, it's important to check any issue related when trying to click it
            except ElementNotFound as ex:
                if show_more_button_xpath in str(ex):
                    print_debug_log("Stopped after no more instances of \"show more\" button")
                else:
                    print_debug_log(f"Stopped after unexpected \"ElementNotFound\" error: {ex}")

                break
            except Exception as ex:
                print_debug_log(f"Stopped after unexpected \"Exception\" error: {ex}")

        articles_count = self.__get_element_count__(articles_xpath)
        print_debug_log(f"Total scrolling of {articles_count} articles")


    def __click_in_show_more_button__(self, show_more_button_xpath, articles_xpath):
        articles_count = self.__get_element_count__(articles_xpath)

        click_tries = 0
        keep_trying = True

        while True:
            try:

                self.__browser__.scroll_element_into_view(show_more_button_xpath)
                self.__browser__.click_button_when_visible(show_more_button_xpath)

                # Let's wait for the page to load more articles
                await_condition = f"return document.querySelectorAll(\"ol[data-testid='search-results'] li[data-testid='search-bodega-result']\").length > {articles_count}"
                self.__browser__.wait_for_condition(await_condition, 10)

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
                    keep_trying = False
                    break
            except Exception as ex:
                print_debug_log(f"Exception when clicking \"show more\" button: {ex}")
                break

        articles_count = self.__get_element_count__(articles_xpath)
        print_debug_log(f"Scrolled through {articles_count} articles")

        return keep_trying
            

    def __get_articles_info__(self, query):
        print_debug_log("Extracting info from articles")

        article_info_list = []

        articles_xpath = "xpath://ol[@data-testid='search-results']//li[@data-testid='search-bodega-result']"
        articles_count = self.__get_element_count__(articles_xpath)

        query_lower = query.lower()

        # Selenium selector starts from 1
        for i in range(1, articles_count + 1):
            try:

                # Using full chained xpath
                # because using element.find_elements to find children
                # only throws exception
                article_children_div_xpath = f"{articles_xpath}[{i}]/div/"
                picture_xpath = f"{article_children_div_xpath}div/figure/div/img"

                title = self.__get_attribute_inner_html__        (f"{article_children_div_xpath}div/div/a/h4")
                date = self.__get_attribute_inner_html__         (f"{article_children_div_xpath}span")
                description = self.__get_attribute_inner_html__  (f"{article_children_div_xpath}div/div/a/p[1]")
                picture_url = None            

                # Some articles do not have image
                if len(self.__browser__.find_elements(picture_xpath)) > 0:
                    picture_url = self.__browser__.find_element(picture_xpath).get_attribute("src")
                
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

            if i % 10 == 0:
                work_percentage_concluded = round(i / articles_count * 100)
                print_debug_log(f"Info extracted from {i}/{articles_count} ({work_percentage_concluded}%) articles")

        print_debug_log(f"Info extracted from all {articles_count} articles")
        
        return article_info_list