from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math


def check_authentic_maturity(issue_date, maturity_date, payment_cycle):
    delta = relativedelta(maturity_date, issue_date)
    months = delta.years * 12 + delta.months
    authenticity_criteria = months % payment_cycle + delta.days
    authenticity = False if authenticity_criteria else True
    return authenticity

day1 = datetime.strptime('20230131', '%Y%m%d')
day2 = datetime.strptime('20230731', '%Y%m%d')
day3 = datetime.strptime('20230228', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)

a = check_authentic_maturity(day1, day2, 3)
print(a)