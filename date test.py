from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta

def get_fv_theoretical(principal, interest_rate, remaining_days):
    interest_rate /= 100
    fv = principal * ((1 + interest_rate) ** (remaining_days / 365))
    return fv

def get_fv_conventional(principal, interest_rate, term_number, remainder_days=None, frequency=None):
    f = frequency
    r = interest_rate / 100
    d = remainder_days if remainder_days is not None else remainder_days

    fv = principal * (((1 + (r / f)) ** term_number) * (1 + (r * (d / 365))))

    return fv

def get_interest(start_date=None, end_date=None, interest_rate=None, payment_cycle=None, frequency=None):
    principal = 10000

    delta = relativedelta(end_date, start_date)
    months = delta.years * 12 + delta.months
    term_number = months // payment_cycle
    last_term_day = start_date + relativedelta(months=payment_cycle) * term_number
    remainder_period = end_date - last_term_day
    remainder_days = remainder_period.days
    principal_interest = get_fv_conventional(principal, interest_rate, term_number, remainder_days, frequency)
    interest = principal_interest - principal
    return interest

day1 = datetime.strptime('20220101', '%Y%m%d')
day2 = datetime.strptime('20230202', '%Y%m%d')
day3 = datetime.strptime('20220907', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')
days = (day2 - day1).days

iC = get_interest(day1, day2, 3.12, 12, 1)
iT = get_fv_theoretical(10000, 3.12, days) - 10000
print(iC)
print(iT)