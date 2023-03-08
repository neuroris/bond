from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

day1 = datetime.strptime('20271028', '%Y%m%d')
day2 = datetime.strptime('20270928', '%Y%m%d')
day3 = datetime.strptime('20230803', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)

days2 = (day3 - day2).days
print(days2)