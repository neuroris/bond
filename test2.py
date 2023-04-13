from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date, time
import math, time

def get_simple_interest_number(start_date, end_date):
    one_year = relativedelta(years=1)
    reference_date = start_date
    simple_interest_number = 0
    while reference_date < end_date:
        next_year = reference_date + one_year
        simple_interest_period = (next_year - reference_date).days
        simple_interest_days = (min(next_year, end_date) - reference_date).days
        simple_interest_number += simple_interest_days / simple_interest_period
        reference_date += one_year
    return simple_interest_number

def get_years(start_date, end_date):
    delta = relativedelta(end_date, start_date)
    quotient_years = delta.years
    last_year = start_date + relativedelta(years=quotient_years)
    next_year = last_year + relativedelta(years=1)
    remaining_days = (end_date - last_year).days
    remaining_term = (next_year - last_year).days
    remaining_years = remaining_days / remaining_term
    years = quotient_years + remaining_years

    return years

day1 = datetime.strptime('20230316', '%Y%m%d')
day2 = datetime.strptime('20280315', '%Y%m%d')

b = time.time()
years = get_simple_interest_number(day1, day2)
a = time.time()
d = a - b
print(d)

b = time.time()
years2 = get_years(day1, day2)
a = time.time()
d = a - b
print(d)

print(years)
print(years2)