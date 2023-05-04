class RPAFilterNames:
    SEARCH_PHRASE = "search_phrase"
    NEWS_CATEGORY_OR_SECTION = "news_category_or_section"
    MONTHS = "months"

class RPADefaultFilters:
    SEARCH_PHRASE = "Economy"
    NEWS_CATEGORY_OR_SECTION = ["Test A", "Business", "Test B", "Opinion", "U.S.", "Week in Review", "World"]
    MONTHS = 2

class URLs:
    WEBSITE = "https://www.nytimes.com/"
    WEBSITE_QUERY = "https://www.nytimes.com/search?query={query}"

class Regexes:
    HOURS_AGO_REGEX = "\d{1,2}h ago"

    CURRENCY_REGEX_LIST = [
        "\$\d{1,3}\.\d{1,2}",           # $11.1
        "\$\d{1,3}\,\d{3}\.\d{1,2}",    # $111,111.11
        "\d{1,3} dollars",              # 11 dollars
        "\d{1,3} usd"                   # 11 USD
    ]

    CURRENCY_REGEX_LIST_JOINED = '(?:%s)' % '|'.join(CURRENCY_REGEX_LIST)

class CSVConstants:
    CSV_HEADER = {
        "title": "Title",
        "date": "Date",
        "description": "Description",
        "picture_filename": "Picture filename",
        "search_phrases_count": "Count of search phrases",
        "contains_money": "Contains money"
    }

    CSV_FIELDNAMES = ["title", "date", "description", "picture_filename", "search_phrases_count", "contains_money"]

class OtherConstants:
    MAX_TRIES_IN_SHOW_MORE_BUTTON = 5


class XPaths:
    MAIN_PAGE_SEARCH_BUTTON = "xpath://button[@data-test-id='search-button']"
    MAIN_PAGE_SEARCH_INPUT ="xpath://input[@data-testid='search-input']"
    MAIN_PAGE_SEARCH_SUBMIT = "xpath://button[@data-test-id='search-submit']"

    COOKIE_WINDOW_CLOSE_BUTTON = "xpath://button[@data-testid='expanded-dock-btn-selector']"

    SEARCH_PAGE_DATE_DROPDOWN = "xpath://button[@data-testid='search-date-dropdown-a']"
    SEARCH_PAGE_SPECIFIC_DATES = "xpath://div[@aria-label='Date Range']//button[@value='Specific Dates']"

    SEARCH_PAGE_SECTION_DROPDOWN = "xpath://button[@data-testid='search-multiselect-button']"
    SEARCH_PAGE_SECTION_SELECTOR = "//span[text()='{news_category}']"
    SEARCH_PAGE_SECTION_ANY_SELECTOR = "//span[text()='Any']"

    SEARCH_PAGE_SORT_BY_SELECTOR = "xpath://select[@data-testid='SearchForm-sortBy']"
    SEARCH_PAGE_SORT_BY_NEWEST = f"{SEARCH_PAGE_SORT_BY_SELECTOR}/option[@value='newest']"

    SEARCH_PAGE_SEARCH_BUTTON = "xpath://button[@data-testid='search-page-submit']"

    SEARCH_PAGE_SHOW_MORE_BUTTON = "xpath://button[@data-testid='search-show-more-button']"

    SEARCH_PAGE_LOAD_ARTICLES_AWAIT_CONDITION = "return document.querySelectorAll(\"ol[data-testid='search-results'] li[data-testid='search-bodega-result']\").length > {articles_count}"

    ARTICLES_LIST = "xpath://ol[@data-testid='search-results']//li[@data-testid='search-bodega-result']"

    # Using full chained xpath because using element.find_elements to find children only throws exception
    ARTICLE_CHILDREN_DIV = f"{ARTICLES_LIST}" + "[{i}]/div/"
    ARTICLE_PICTURE = f"{ARTICLE_CHILDREN_DIV}div/figure/div/img"
    ARTICLE_TITLE = f"{ARTICLE_CHILDREN_DIV}div/div/a/h4"
    ARTICLE_DATE = f"{ARTICLE_CHILDREN_DIV}span"
    ARTICLE_DESCRIPTION = f"{ARTICLE_CHILDREN_DIV}div/div/a/p[1]"