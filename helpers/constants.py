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