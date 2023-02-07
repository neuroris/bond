from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

day1 = datetime.strptime('20231216', '%Y%m%d')
day2 = datetime.strptime('20241215', '%Y%m%d')
day3 = datetime.strptime('20230228', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)

for i in range(365):
    day = day1 + relativedelta(days=i)
    days = (day2 - day).days
    print(day, days)