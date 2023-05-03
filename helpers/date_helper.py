import default_variables

# Importing date libs
import datetime, re, calendar
from dateutil.relativedelta import relativedelta

def fixing_months_variable(months):
    if not type(months) == int:
        months = default_variables.MONTHS
    elif months < 0:
        months = default_variables.MONTHS

    return months

def calculate_start_and_end_date(months):
    today = datetime.datetime.now()

    # Adding one day because of how nyt website works
    start_date_string = None
    end_date_string = (today + datetime.timedelta(days=1)).strftime("%m/%d/%Y")

    # Applying rules
    if months == 0 or months == 1:
        first_day_of_month = today.replace(day=1)
    else:
        start_month = today - relativedelta(months=months - 1)
        first_day_of_month = start_month.replace(day=1)

    start_date_string = (first_day_of_month + datetime.timedelta(days=1)).strftime("%m/%d/%Y")

    return start_date_string, end_date_string

def convert_hours_ago_label_to_today_date(date):
    if len(re.findall(default_variables.HOURS_AGO_REGEX, date)) > 0:
        today = datetime.datetime.now()
        return f"{calendar.month_abbr[today.month]} {today.day}"
    else:
        return date