from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
import math

class Bond:
    def __init__(self, coupon_rate, given_price, face_value, payment_cycle, amount, discount_rate,
                 maturity_date, outset_date='', issue_date=''):
        self.payment_cycle = payment_cycle
        self.frequency = int(12 / payment_cycle)
        self.coupon = int(((face_value * (coupon_rate * 1000) * amount / self.frequency) / 100) / 1000)
        self.coupon_rate = coupon_rate
        self.given_price = given_price
        self.face_value = face_value
        self.maturity_value = face_value * amount
        self.purchase_value = given_price * amount
        self.amount = amount
        self.given_discount_rate = discount_rate
        self.maturity_date = datetime.strptime(maturity_date, '%Y%m%d')
        self.outset_date = datetime.strptime(outset_date, '%Y%m%d') if outset_date else datetime.combine(date.today(), time.min)
        self.issue_date = datetime.strptime(issue_date, '%Y%m%d') if issue_date else None
        self.authentic_maturity_date = self.maturity_date.replace(day=self.issue_date.day) if issue_date else self.maturity_date

        self.remaining_days = self.get_remaining_days()
        self.remaining_delta = relativedelta(self.maturity_date, self.outset_date)
        self.coupon_period = 365 / self.frequency
        self.term = relativedelta(months=payment_cycle)

        self.authentic_delta = relativedelta(self.authentic_maturity_date, self.outset_date)
        remaining_months = self.authentic_delta.years * 12 + self.authentic_delta.months + self.authentic_delta.days / 31
        self.term_number = math.ceil(remaining_months / self.payment_cycle - 1)
        self.coupon_number = self.term_number + 1

        self.previous_coupon_date = self.authentic_maturity_date - self.coupon_number * self.term
        self.coupon_days = self.get_coupon_days()
        # self.remainder_days = self.remaining_days - round(self.term_number * self.coupon_period)
        # self.remainder_days = int(self.remaining_days % self.coupon_period)
        self.remainder_days = self.get_remainder_days()
        self.interest_income = self.get_interest_income()
        self.tax = self.get_tax()
        self.last_coupon = 0
        self.capital_income = 0
        self.total_income = 0
        self.profit = 0.0
        self.profit_rate = 0.0
        self.profit_rate_annual = 0.0
        self.CAGR = 0.0
        self.profit_rate_bank = 0.0

        self.price = 0
        self.discount_rate = 0

    def get_remaining_days(self):
        day_span_date = self.maturity_date - self.outset_date
        day_span = abs(day_span_date.days)
        return day_span

    def get_remainder_days(self):
        first_coupon_date = self.coupon_days[0]
        remainder_period = first_coupon_date - self.outset_date
        remainder_days = remainder_period.days
        return remainder_days

    def get_coupon_days(self):
        coupon_days = list()
        coupon_day = self.previous_coupon_date
        for coupon_index in range(self.term_number):
            coupon_day += self.term
            coupon_days.append(coupon_day)
        coupon_days.append(self.maturity_date)
        return coupon_days

    def get_interest_income(self):
        if self.maturity_date == self.authentic_maturity_date:
            self.last_coupon = self.coupon
            interest_income = self.coupon * self.coupon_number
        else:
            before_last_coupon_date = self.coupon_days[-2] if self.coupon_number >= 2 else self.previous_coupon_date
            last_period = self.maturity_date - before_last_coupon_date
            self.last_coupon = int(self.coupon * self.frequency * (last_period.days / 365))
            interest_income = self.coupon * (self.coupon_number - 1) + self.last_coupon
        return interest_income

    def get_tax(self):
        first_coupon_date = self.coupon_days[0]
        first_period = first_coupon_date - self.previous_coupon_date
        first_imposing_period = first_coupon_date - self.outset_date
        first_tax_base = int(self.coupon * (first_imposing_period.days / first_period.days))
        first_tax = self.calculate_tax(first_tax_base)
        middle_tax = self.calculate_tax(self.coupon) * (self.coupon_number - 2) if self.coupon_number >= 3 else 0
        last_tax = self.calculate_tax(self.last_coupon) if self.coupon_number >= 2 else 0
        tax = first_tax + middle_tax + last_tax
        return tax

    def calculate_tax(self, tax_base):
        income_tax = int(tax_base * 0.14 / 10) * 10
        residence_tax = int(income_tax * 0.1 / 10) * 10
        total_tax = income_tax + residence_tax
        return total_tax

    def get_CAGR(self, current_value, future_value, elapsed_days):
        CAGR = ((future_value / current_value) ** (1 / (elapsed_days / 365))) - 1
        return CAGR

    def get_dcv_theoretical(self, future_value, discount_rate=None, remaining_days=None, frequency=None):
        remaining_days = remaining_days if remaining_days is not None else self.remaining_days
        discount_rate = discount_rate if discount_rate is not None else self.given_discount_rate
        frequency = frequency if frequency else self.frequency
        discount_rate /= 100

        dcv = future_value / \
              ((1 + (discount_rate / frequency)) ** (remaining_days / 365 * frequency))

        return dcv

    def get_dcv_conventional(self, future_value, discount_rate, term_number, remainder_days=None, frequency=None):
        f = frequency if frequency else self.frequency
        r = discount_rate / 100
        d = remainder_days if remainder_days else self.remainder_days

        dcv = future_value / \
              (((1 + r / f) ** term_number) * (1 + r * (d / 365)))

        return dcv

    def get_price_base(self, get_dcv_func, discount_rate):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        discount_rate /= (self.frequency * 100)

        price = 0
        for period_index in range(self.term_number):
            point_remaining_day = self.remainder_days + self.coupon_period * period_index
            point_dcv = get_dcv_func(self.coupon, point_remaining_day, discount_rate)
            price += point_dcv
        maturation_dcv = get_dcv_func(self.coupon + self.maturity_value, self.remaining_days, discount_rate)
        price += maturation_dcv

        return price

    def get_price_theoretical_deprecated(self, discount_rate=None):
        price = self.get_price_base(self.get_dcv_theoretical, discount_rate)
        return price

    def get_price_deprecated(self, discount_rate=None):
        price = self.get_price_base(self.get_dcv, discount_rate)
        return price

    def get_price_theoretical(self, discount_rate):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_date in self.coupon_days:
            remaining_period = coupon_date - self.outset_date
            remaining_days = remaining_period.days
            price += self.get_dcv_theoretical(self.coupon, discount_rate, remaining_days)
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, self.remaining_days)
        return price

    def get_price_conventional(self, discount_rate):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_index in range(self.coupon_number):
            price += self.get_dcv_conventional(self.coupon, discount_rate, coupon_index)
        price += self.get_dcv_conventional(self.maturity_value, discount_rate, self.term_number)
        return price

    def calculate_theoretical_price(self, coupon, maturity_value, discount_rate, total_remaining_days, frequency):
        coupon_period = 365 / frequency
        coupon_number = math.ceil(total_remaining_days / coupon_period)
        term_number = coupon_number - 1
        remainder_days = total_remaining_days - coupon_period * term_number

        price = 0
        remaining_days = 0
        for coupon_index in range(coupon_number):
            remaining_days = remainder_days + coupon_period * coupon_index
            price += self.get_dcv_theoretical(coupon, discount_rate, remaining_days, frequency)
        price += self.get_dcv_theoretical(maturity_value, discount_rate, remaining_days, frequency)
        return price

    def calculate_conventional_price(self, coupon, maturity_value, discount_rate, total_remaining_days, frequency):
        coupon_period = 365 / frequency
        coupon_number = math.ceil(total_remaining_days / coupon_period)
        term_number = coupon_number - 1
        remainder_days = total_remaining_days - coupon_period * term_number

        price = 0
        for coupon_index in range(coupon_number):
            price += self.get_dcv_conventional(coupon, discount_rate, coupon_index, remainder_days, frequency)
        price += self.get_dcv_conventional(maturity_value, discount_rate, term_number, remainder_days, frequency)
        return price

    def get_discount_rate_base(self, get_price_func, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate_max = 100
        discount_rate = discount_rate_max / 2
        searching_gap = discount_rate_max / 2
        searching_number = 0
        while searching_number < 10000:
            searching_number += 1
            searching_gap /= 2
            dcv = get_price_func(discount_rate)
            rounded_dcv = round(dcv, 6)
            if rounded_dcv > purchase_value:
                discount_rate += searching_gap
            elif rounded_dcv < purchase_value:
                discount_rate -= searching_gap
            else:
                break
        rounded_discount_rate = round(discount_rate , 3)
        return rounded_discount_rate

    def get_discount_rate_theoretical(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_theoretical, purchase_value)
        return discount_rate

    def get_discount_rate(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_conventional, purchase_value)
        # discount_rate = self.get_discount_rate_base(self.get_price_theoretical, purchase_value)
        return discount_rate

    def calculate_discount_rate_engine(self, get_price_func, price, coupon, maturity_value, remaining_days, frequency):
        discount_rate_max = 100
        discount_rate = discount_rate_max / 2
        searching_gap = discount_rate_max / 2
        searching_number = 0
        while searching_number < 10000:
            searching_number += 1
            searching_gap /= 2
            dcv = get_price_func(coupon, maturity_value, discount_rate, remaining_days, frequency)
            rounded_dcv = round(dcv, 6)
            if rounded_dcv > price:
                discount_rate += searching_gap
            elif rounded_dcv < price:
                discount_rate -= searching_gap
            else:
                break
        rounded_discount_rate = round(discount_rate, 3)
        return rounded_discount_rate

    def calculate_theoretical_discount_rate(self, price, coupon, maturity_value, remaining_days, frequency):
        discount_rate = self.calculate_discount_rate_engine\
            (self.calculate_theoretical_price, price, coupon, maturity_value, remaining_days, frequency)
        return discount_rate

    def calculate_conventional_discount_rate(self, price, coupon, maturity_value, remaining_days, frequency):
        discount_rate = self.calculate_discount_rate_engine\
            (self.calculate_conventional_price, price, coupon, maturity_value, remaining_days, frequency)
        return discount_rate

    def analyze_price(self):
        self.price = self.get_price_conventional() / self.amount
        self.discount_rate = self.given_discount_rate

        print('=================================================')
        print('      Price Analysis (discount rate: {}%)      '.format(self.given_discount_rate))
        print('=================================================')
        self.report()
        print('\033[095mprice: {:,}\033[0m'.format(self.price))
        print('=================================================')

    def analyze_discount_rate(self):
        self.price = self.given_price
        self.discount_rate = self.get_discount_rate()

        print('=================================================')
        print('      Discount Rate Analysis (price: {})      '.format(self.given_price))
        print('=================================================')
        self.report()
        print('\033[095mdiscount_rate: {}%\033[0m'.format(self.discount_rate))
        print('=================================================')

    def report(self):
        self.capital_income = int(self.maturity_value - self.price * self.amount)
        self.total_income = self.interest_income + self.capital_income
        self.profit = self.total_income - self.tax
        self.profit_rate = self.profit / (self.price * self.amount) * 100
        self.profit_rate_annual = self.profit_rate / (self.remaining_days / 365)
        self.CAGR = self.get_CAGR(self.price * self.amount, self.price * self.amount + self.profit, self.remaining_days) * 100
        self.profit_rate_bank = self.profit_rate_annual / 0.846

        print('outset date:', self.outset_date.strftime('%Y-%m-%d'))
        print('maturity date:', self.maturity_date.strftime('%Y-%m-%d'))
        print('remaining days: {} ({} years, {} months, {} days)'.
              format(self.remaining_days, self.remaining_delta.years, self.remaining_delta.months, self.remaining_delta.days))
        print('price: {:,.2f}'.format(self.price))
        print('face value: {:,}'.format(self.face_value))
        print('coupon: {:,}'.format(self.coupon))
        print('coupon rate: {:,.3f}%'.format(self.coupon_rate))
        print('coupon number: {:,}'.format(self.coupon_number))
        print('interest income: {:,}'.format(self.interest_income))
        print('capital income: {:,}'.format(self.capital_income))
        print('total income: {:,}'.format(self.total_income))
        print('tax: {:,}'.format(self.tax))
        print('profit: {:,}'.format(self.profit))
        print('profit rate: {:,.3f}%'.format(self.profit_rate))
        print('profit rate(annual): {:,.3f}%'.format(self.profit_rate_annual))
        print('profit rate(bank): {:,.3f}%'.format(self.profit_rate_bank))
        print('profit rate(CAGR): {:,.3f}%'.format(self.CAGR))

# Bond information
given_price = 10011
coupon_rate = 6.043
face_value = 10000
payment_cycle = 3
amount = 100
given_discount_rate = 25.127
maturity_date = '20241025'
outset_date = '20221202'
issue_date = '20221027'

# Simple calculation
# coupon = 151.075
# future_value = 10000
# current_value = 10011
# discount_rate = 6.323
# remaining_days = 693
# frequency = 4

coupon = 500
future_value = 10000
current_value = 10000
discount_rate = 10
remaining_days = 365
frequency = 2

bond = Bond(coupon_rate, given_price, face_value, payment_cycle, amount, given_discount_rate,
            maturity_date, outset_date, issue_date)

# bond.analyze_price()
bond.analyze_discount_rate()

# dcv = bond.get_dcv_theoretical(future_value, discount_rate, remaining_days, frequency)
# dcv = bond.get_dcv_conventional(future_value, discount_rate, remaining_days, frequency)
# print(dcv)

price_T = bond.calculate_theoretical_price(coupon, future_value, discount_rate, remaining_days, frequency)
price_C = bond.calculate_conventional_price(coupon, future_value, discount_rate, remaining_days, frequency)
print('price(T)', price_T)
print('price(C)', price_C)
discount_rate_T = bond.calculate_theoretical_discount_rate(current_value, coupon, future_value, remaining_days, frequency)
discount_rate_C = bond.calculate_conventional_discount_rate(current_value, coupon, future_value, remaining_days, frequency)
print('Discount rate(T)', discount_rate_T)
print('Discount rate(C)', discount_rate_C)