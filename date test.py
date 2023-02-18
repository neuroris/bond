from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

day1 = datetime.strptime('20250228', '%Y%m%d')
day2 = datetime.strptime('20250228', '%Y%m%d')
day3 = datetime.strptime('20240228', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)

d = (day2 - day1 - day3).days
print(d)