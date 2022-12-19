from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

day1 = datetime.strptime('20221102', '%Y%m%d')
day2 = datetime.strptime('20251101', '%Y%m%d')
day3 = datetime.strptime('20221229', '%Y%m%d')
day4 = datetime.strptime('20230329', '%Y%m%d')
today = datetime.today().strftime('%Y%m%d')

r = relativedelta(day2, day1)
# r_mon = r.years * 12 + r.months + r.days / 31
r_mon = r.years * 12 + r.months
t = int(r_mon / 12)
print(r)
print(r_mon)
print(t)

