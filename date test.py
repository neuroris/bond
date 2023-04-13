from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math


def check_authenticity(issue_date, end_date):
    payment_cycle = 12
    delta = relativedelta(end_date, issue_date)
    months = delta.years * 12 + delta.months
    remainder = months % payment_cycle + delta.days
    authenticity = False if remainder else True
    return authenticity

def check_authenticity2(issue_date, end_date):
    payment_cycle = 12
    delta = relativedelta(end_date, issue_date)
    months = delta.years * 12 + delta.months
    virtual_issue_date = end_date - relativedelta(months=months)
    authenticity = True if virtual_issue_date == issue_date else False
    return authenticity

def get_term_days(start_date, end_date, payment_cycle):
    delta = relativedelta(end_date, start_date)
    months = delta.years * 12 + delta.months
    term_number = months // payment_cycle
    term_end_date = start_date + term_number * relativedelta(months=payment_cycle)
    remainder_days = (end_date - term_end_date).days
    if start_date.month == 2 and start_date.day == 28 and end_date.month == 2 and end_date.day == 29:
        remainder_days = 0

    return term_number, remainder_days

def get_term(start_date, term_number, payment_cycle):
    payment_delta = relativedelta(months=payment_cycle)
    previous_term_date = start_date + term_number * payment_delta
    next_term_date = previous_term_date + payment_delta
    term = (next_term_date - previous_term_date).days
    return term

def get_interest(principal, start_date=None, end_date=None, interest_rate=None, payment_cycle=None):
    frequency = 12 / payment_cycle

    term_number, remainder_days = get_term_days(start_date, end_date, payment_cycle)
    term = get_term(start_date, term_number)
    term_days = term * term_number
    remaining_days = term_days + remainder_days
    principal_interest = get_fv_theoretical(principal, interest_rate, remaining_days, frequency, term)
    interest = principal_interest - principal
    return interest

def get_fv_theoretical(principal, interest_rate, remaining_days, frequency=None, term=None):
    f = frequency if frequency else self.frequency
    r = interest_rate / 100
    term = 365 / frequency if not term else term

    fv = principal * ((1 + (r / f)) ** (remaining_days / term))

    return fv

day1 = datetime.strptime('20240229', '%Y%m%d')
day2 = datetime.strptime('20290228', '%Y%m%d')
day3 = datetime.strptime('20230803', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)

day = day2 - relativedelta(months=12)
print(day)

authenticity = check_authenticity(day1, day2)
authenticity2 = check_authenticity2(day1, day2)
print(authenticity)
print(authenticity2)