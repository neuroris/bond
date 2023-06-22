from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

day1 = datetime.strptime('20230425', '%Y%m%d')
day2 = datetime.strptime('20230831', '%Y%m%d')
day3 = datetime.strptime('20230803', '%Y%m%d')
day4 = datetime.strptime('20230527', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

days = (day2 - day1).days
delta = relativedelta(day2, day1)
print(days)
print(delta)
