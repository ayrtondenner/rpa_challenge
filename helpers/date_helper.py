from helpers.constants import RPADefaultFilters, Regexes
from helpers.debug_helper import print_debug_log

# Importing date libs
import datetime, re, calendar
from dateutil.relativedelta import relativedelta

def fixing_months_variable(months):
    """Fixing 'months' filter

    Args:
        months (int): the months filter in number

    Returns:
        int: the months filter int after fixing it
    """
    try:
        if not type(months) == int:
            months = RPADefaultFilters.MONTHS
        elif months < 0:
            months = RPADefaultFilters.MONTHS

        return months
    except Exception as ex:
        print_debug_log(f"Error when parsing months variable '{months}'")
        return months

def calculate_start_and_end_date(months):
    """Calculates start and end date depending on the months integer filter.
    The start date will be the first day of the first month.
    The end date will be the current day
    
    Args:
        months (int): the months int filter

    Returns:
        str, str: the start and end date as strings
    """
    today = datetime.datetime.now()

    # Adding one day because of how nyt website works
    start_date_string = None
    end_date = today + datetime.timedelta(days=1)
    end_date_string = end_date.strftime("%m/%d/%Y")

    try:
        # Applying rules
        if months == 0 or months == 1:
            first_day_of_month = today.replace(day=1)
        else:
            start_month = today - relativedelta(months=months - 1)
            first_day_of_month = start_month.replace(day=1)

        start_date = first_day_of_month + datetime.timedelta(days=1)
        start_date_string = start_date.strftime("%m/%d/%Y")

        assert start_date < end_date, f"Start date {start_date_string} is not smaller than end date {end_date_string}!"

        return start_date_string, end_date_string
    except Exception as ex:
        print_debug_log(f"Error when calculating start and end date from months variable '{months}': {ex}")
        start_date_string = end_date_string
    finally:
        return start_date_string, end_date_string

def convert_hours_ago_label_to_today_date(date):
    """When an article was posted today, NYTimes doesn't show the date, but a "hours ago" label.
    Example: 3h ago -> 5 May.

    Args:
        date (str): the date label

    Returns:
        str: the date label after the fix
    """
    try:
        if len(re.findall(Regexes.HOURS_AGO_REGEX, date)) > 0:
            today = datetime.datetime.now()
            return f"{calendar.month_abbr[today.month]} {today.day}"
        else:
            return date
    except Exception as ex:
        print_debug_log(f"Error when parsing date variable '{date}'")
        return date