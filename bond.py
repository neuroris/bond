from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from items import *
import math

class BondItem():
    def __init__(self):
        self.name = ''
        self.type = ''
        self.given_price = 10000
        self.given_discount_rate = 10.0
        self.coupon_rate = 0.0
        self.face_value = 10000
        self.payment_cycle = 12
        self.amount = 0
        self.issue_date = ''
        self.maturity_date = ''
        self.outset_date = ''
        self.compound_interest = False
        self.compound_interest_number = 0
        self.simple_interest_number = 0

    def set(self, item):
        self.name = item['name']
        self.type = item['type']
        self.given_price = item['price']
        self.given_discount_rate = item['discount rate']
        self.coupon_rate = item['coupon rate']
        self.face_value = item['face value']
        self.payment_cycle = item['payment cycle']
        self.amount = item['amount']
        self.issue_date = item['issue date']
        self.maturity_date = item['maturity date']
        self.outset_date = item['outset date']
        self.compound_interest = item['compound interest']
        self.compound_interest_number = item['compound interest number']
        self.simple_interest_number = item['simple interest number']

class Bond:
    def __init__(self, item):
        self.last_coupon = 0
        self.capital_income = 0
        self.total_income = 0
        self.profit = 0.0
        self.profit_rate = 0.0
        self.profit_rate_annual = 0.0
        self.CAGR = 0.0
        self.CAGR_bank = 0.0
        self.profit_rate_bank = 0.0
        self.first_tax = 0
        self.middle_tax = 0
        self.last_tax = 0
        self.first_tax_base = 0
        self.middle_tax_base = 0
        self.last_tax_base = 0

        self.price = 0
        self.price_wook = 0
        self.price_wook_tax = 0
        self.price_wook_tax_bank = 0
        self.discount_rate = 0.0
        self.discount_rate_tax = 0.0
        self.discount_rate_wook = 0.0
        self.discount_rate_wook_tax = 0.0

        self.name = item.name
        self.type = item.type
        self.payment_cycle = item.payment_cycle
        self.frequency = int(12 / item.payment_cycle)
        self.compound_interest = item.compound_interest
        self.compound_interest_number = item.compound_interest_number
        self.simple_interest_number = item.simple_interest_number
        self.coupon_rate = item.coupon_rate
        self.given_price = item.given_price
        self.face_value = item.face_value
        self.maturity_value = item.face_value * item.amount
        self.purchase_value = item.given_price * item.amount
        self.amount = item.amount
        self.given_discount_rate = item.given_discount_rate
        self.maturity_date = datetime.strptime(item.maturity_date, '%Y%m%d')
        self.outset_date = datetime.strptime(item.outset_date, '%Y%m%d') if item.outset_date else datetime.combine(date.today(), time.min)
        self.issue_date = datetime.strptime(item.issue_date, '%Y%m%d') if item.issue_date else None
        self.authentic_maturity_date = self.maturity_date.replace(day=self.issue_date.day) if item.issue_date else self.maturity_date
        self.remaining_days = self.get_remaining_days()
        self.remaining_delta = relativedelta(self.maturity_date, self.outset_date)
        self.coupon_period = 365 / self.frequency
        self.term = relativedelta(months=item.payment_cycle)
        self.authentic_delta = relativedelta(self.authentic_maturity_date, self.outset_date)
        self.term_number = self.get_term_number()
        self.coupon_number = self.term_number + 1
        self.previous_coupon_date = self.get_previous_coupon_date()
        self.coupon_days = self.get_coupon_days()
        self.remainder_days = self.get_remainder_days()
        self.coupon = self.get_coupon()
        self.interest_income = self.get_interest_income()
        self.tax = self.get_tax()

    def get_term_number(self):
        remaining_months = self.authentic_delta.years * 12 + self.authentic_delta.months + self.authentic_delta.days / 31
        term_number = math.ceil(remaining_months / self.payment_cycle - 1) if not self.compound_interest else 0
        return term_number

    def get_remaining_days(self):
        day_span_date = self.maturity_date - self.outset_date
        day_span = abs(day_span_date.days)
        return day_span

    def get_remainder_days(self):
        first_coupon_date = self.coupon_days[0]
        remainder_period = first_coupon_date - self.outset_date
        remainder_days = remainder_period.days
        return remainder_days

    def get_previous_coupon_date(self):
        outset_issue_delta = relativedelta(self.outset_date, self.issue_date)
        outset_issue_months = outset_issue_delta.years * 12 + outset_issue_delta.months
        prepaid_count = outset_issue_months // self.payment_cycle
        previous_coupon_date = self.issue_date + self.term * prepaid_count if not self.compound_interest else self.issue_date
        return previous_coupon_date

    def get_coupon_days(self):
        coupon_days = list()
        coupon_day = self.previous_coupon_date
        for coupon_index in range(self.term_number):
            coupon_day += self.term
            coupon_days.append(coupon_day)
        coupon_days.append(self.maturity_date)
        return coupon_days

    def get_coupon(self):
        if self.compound_interest:
            total_period = self.maturity_date - self.issue_date
            # total_remaining_days = total_period.days
            # future_value = self.get_fv_theoretical(10000, self.coupon_rate, total_remaining_days)
            future_value = self.get_interest(10000, self.issue_date, self.maturity_date, self.coupon_rate) + 10000
            coupon = int(future_value - 10000) * self.amount
        else:
            coupon = int(((self.face_value * (self.coupon_rate * 1000) * self.amount / self.frequency) / 100) / 1000)
        return coupon

    def get_interest_income(self):
        before_last_coupon_date = self.coupon_days[-2] if self.coupon_number >= 2 else self.previous_coupon_date
        virtual_before_last_coupon_date = self.authentic_maturity_date - self.term
        if (virtual_before_last_coupon_date == before_last_coupon_date) and (self.maturity_date == self.authentic_maturity_date)\
                or self.compound_interest:
            self.last_coupon = self.coupon
            interest_income = self.coupon * self.coupon_number
        else:
            coupon = self.maturity_value * (self.coupon_rate / 100)
            last_period = self.maturity_date - before_last_coupon_date
            self.last_coupon = int(coupon * (last_period.days / 365))
            interest_income = self.coupon * (self.coupon_number - 1) + self.last_coupon
        return interest_income

    def get_tax(self):
        first_coupon_date = self.coupon_days[0]
        first_period = first_coupon_date - self.previous_coupon_date
        first_imposing_period = first_coupon_date - self.outset_date

        if self.compound_interest:
            deduction_days = first_period.days - first_imposing_period.days
            coupon_deduction_unit = self.get_fv_theoretical(10000, self.coupon_rate, deduction_days) - 10000
            coupon_deduction = coupon_deduction_unit * self.amount
            tax_base = int(self.coupon - coupon_deduction)
            self.first_tax_base = tax_base
            self.first_tax = self.calculate_tax(tax_base)
            tax = self.first_tax
        else:
            coupon = (self.maturity_value / self.frequency) * (self.coupon_rate / 100)
            first_tax_base = round(coupon * (first_imposing_period.days / first_period.days))
            self.first_tax_base = first_tax_base
            self.first_tax = self.calculate_tax(first_tax_base)
            self.middle_tax_base = self.coupon
            self.middle_tax = self.calculate_tax(coupon) if self.coupon_number >= 3 else 0
            self.last_tax_base = self.last_coupon
            self.last_tax = self.calculate_tax(self.last_coupon) if self.coupon_number >= 2 else 0
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        return tax

    def calculate_tax(self, tax_base):
        income_tax = int(tax_base * 0.14 / 10) * 10
        residence_tax = int(income_tax * 0.1 / 10) * 10
        total_tax = income_tax + residence_tax
        return total_tax

    def get_CAGR(self, current_value, future_value, elapsed_days):
        CAGR = ((future_value / current_value) ** (1 / (elapsed_days / 365))) - 1
        return CAGR

    def get_fv_theoretical(self, principal, interest_rate, remaining_days):
        interest_rate /= 100
        fv = principal * ((1 + interest_rate) ** (remaining_days / 365))
        return fv

    def get_fv_conventional(self, principal, interest_rate, term_number, remainder_days=None, frequency=None):
        f = frequency if frequency else self.frequency
        r = interest_rate / 100
        d = remainder_days if remainder_days is not None else self.remainder_days

        fv = principal * (((1 + (r / f)) ** term_number) * (1 + (r * (d / 365))))

        return fv

    def get_interest(self, principal, start_date=None, end_date=None, interest_rate=None, payment_cycle=None, frequency=None):
        start_date = start_date if start_date else self.issue_date
        end_date = end_date if end_date else self.maturity_date
        interest_rate = interest_rate if interest_rate else self.coupon_rate
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        frequency = frequency if frequency else self.frequency

        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        last_term_day = start_date + relativedelta(months=payment_cycle) * term_number
        remainder_period = end_date - last_term_day
        remainder_days = remainder_period.days
        principal_interest = self.get_fv_conventional(principal, interest_rate, term_number, remainder_days, frequency)
        interest = principal_interest - principal
        return interest

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

    def get_price_theoretical(self, discount_rate):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_date in self.coupon_days:
            remaining_period = coupon_date - self.outset_date
            remaining_days = remaining_period.days
            price += self.get_dcv_theoretical(self.coupon, discount_rate, remaining_days)
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, self.remaining_days)
        return price

    def get_price_conventional(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_index in range(self.coupon_number):
            price += self.get_dcv_conventional(self.coupon, discount_rate, coupon_index)
        price += self.get_dcv_conventional(self.maturity_value, discount_rate, self.term_number)
        return price

    def get_price_conventional_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0

        # First term
        first_income = self.coupon - self.first_tax
        price += self.get_dcv_conventional(first_income, discount_rate, 0)

        # Mid term
        if self.coupon_number >= 3:
            for coupon_index in range(1, self.coupon_number - 1):
                middle_income = self.coupon - self.middle_tax
                price += self.get_dcv_conventional(middle_income, discount_rate, coupon_index)

        # Last term
        if self.coupon_number >= 2:
            last_income = self.last_coupon - self.last_tax
            price += self.get_dcv_conventional(last_income, discount_rate, self.term_number)

        # Maturity value
        price += self.get_dcv_conventional(self.maturity_value, discount_rate, self.term_number)
        return price

    def get_price_wook(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_date in self.coupon_days:
            remaining_period = coupon_date - self.outset_date
            remaining_days = remaining_period.days
            price += self.get_dcv_theoretical(self.coupon, discount_rate, remaining_days, 1)
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, self.remaining_days, 1)
        return price

    def get_price_wook_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0

        # First term
        first_coupon_date = self.coupon_days[0]
        remaining_period = first_coupon_date - self.outset_date
        remaining_days = remaining_period.days
        first_income = self.coupon - self.first_tax
        price += self.get_dcv_theoretical(first_income, discount_rate, remaining_days, 1)

        # Mid term
        if self.coupon_number >= 3:
            for coupon_date in self.coupon_days[1:-1]:
                remaining_period = coupon_date - self.outset_date
                remaining_days = remaining_period.days
                middle_income = self.coupon - self.middle_tax
                price += self.get_dcv_theoretical(middle_income, discount_rate, remaining_days, 1)

        # Last term
        if self.coupon_number >= 2:
            last_coupon_date = self.coupon_days[-1]
            remaining_period = last_coupon_date - self.outset_date
            remaining_days = remaining_period.days
            last_income = self.last_coupon - self.last_tax
            price += self.get_dcv_theoretical(last_income, discount_rate, remaining_days, 1)

        # Maturity value
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, self.remaining_days, 1)
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

    def calculate_wook_price(self, coupon, maturity_value, discount_rate, total_remaining_days, frequency):
        coupon_period = 365 / frequency
        coupon_number = math.ceil(total_remaining_days / coupon_period)
        term_number = coupon_number - 1
        remainder_days = total_remaining_days - coupon_period * term_number

        price = 0
        remaining_days = 0
        for coupon_index in range(coupon_number):
            remaining_days = remainder_days + coupon_period * coupon_index
            # price += self.get_dcv_theoretical(coupon, discount_rate, remaining_days, frequency)
            price += self.get_dcv_theoretical(coupon, discount_rate, remaining_days, 1)
        # price += self.get_dcv_theoretical(maturity_value, discount_rate, remaining_days, frequency)
        price += self.get_dcv_theoretical(maturity_value, discount_rate, remaining_days, 1)
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

    def get_discount_rate(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_conventional, purchase_value)
        # discount_rate = self.get_discount_rate_base(self.get_price_theoretical, purchase_value)
        return discount_rate

    def get_discount_rate_tax(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_conventional_tax, purchase_value)
        return discount_rate

    def get_discount_rate_theoretical(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_theoretical, purchase_value)
        return discount_rate

    def get_discount_rate_wook(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_wook, purchase_value)
        return discount_rate

    def get_discount_rate_wook_tax(self, purchase_value=None):
        discount_rate = self.get_discount_rate_base(self.get_price_wook_tax, purchase_value)
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

    def calculate_wook_discount_rate(self, price, coupon, maturity_value, remaining_days, frequency):
        discount_rate = self.calculate_discount_rate_engine\
            (self.calculate_wook_price, price, coupon, maturity_value, remaining_days, frequency)
        return discount_rate

    def analyze_price(self):
        self.discount_rate = self.given_discount_rate
        self.price = self.get_price_conventional() / self.amount
        self.price_wook = self.get_price_wook() / self.amount
        self.price_wook_tax = self.get_price_wook_tax() / self.amount

        print('=================================================')
        print('      Price Analysis (discount rate: {}%)      '.format(self.given_discount_rate))
        print('=================================================')
        self.report()
        print('\033[095mprice(C): {:,}\033[0m'.format(self.price))
        print('\033[093mprice(W): {:,}\033[0m'.format(self.price_wook))
        print('\033[093mprice(T): {:,}\033[0m'.format(self.price_wook_tax))
        print('=================================================')

    def analyze_discount_rate(self):
        self.price = self.given_price
        self.discount_rate = self.get_discount_rate()
        self.discount_rate_tax = self.get_discount_rate_tax()
        self.discount_rate_tax_bank = round(self.discount_rate_tax / 0.846, 3)
        self.discount_rate_wook = self.get_discount_rate_wook()
        self.discount_rate_wook_tax = self.get_discount_rate_wook_tax()
        self.discount_rate_wook_tax_bank = round(self.discount_rate_wook_tax / 0.846, 3)

        print('=================================================')
        print('      Discount Rate Analysis (price: {})      '.format(self.given_price))
        print('=================================================')
        self.report()
        print('\033[095mdiscount_rate(C): {}%\033[0m'.format(self.discount_rate))
        print('\033[095mdiscount_rate(T): {}%\033[0m'.format(self.discount_rate_tax))
        print('\033[095mdiscount_rate(B): {}%\033[0m'.format(self.discount_rate_tax_bank))
        print('\033[093mdiscount_rate(W): {}%\033[0m'.format(self.discount_rate_wook))
        print('\033[093mdiscount_rate(T): {}%\033[0m'.format(self.discount_rate_wook_tax))
        print('\033[093mdiscount_rate(B): {}%\033[0m'.format(self.discount_rate_wook_tax_bank))
        print('=================================================')

    def report(self):
        self.capital_income = int(self.maturity_value - self.price * self.amount)
        self.total_income = self.interest_income + self.capital_income
        self.profit = self.total_income - self.tax
        self.profit_rate = self.profit / (self.price * self.amount) * 100
        self.profit_rate_annual = self.profit_rate / (self.remaining_days / 365)
        self.profit_rate_bank = int(self.profit_rate_annual / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(self.price * self.amount, self.price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

        print('name:', self.name)
        print('issue date:', self.issue_date.strftime('%Y-%m-%d'))
        print('outset date:', self.outset_date.strftime('%Y-%m-%d'))
        print('maturity date:', self.maturity_date.strftime('%Y-%m-%d'))
        print('remaining days: {} ({} years, {} months, {} days) ({} years, {} days)'.
              format(self.remaining_days, self.remaining_delta.years, self.remaining_delta.months, self.remaining_delta.days,
                     self.remaining_delta.years, self.remaining_days - self.remaining_delta.years * 365))
        print('price: {:,.2f}'.format(self.price))
        print('face value: {:,}'.format(self.face_value))
        print('coupon rate: {:,.3f}%'.format(self.coupon_rate))
        print('coupon number: {:,}'.format(self.coupon_number))
        # print('first coupon: {:,} ({})'.format(self.coupon, self.first_tax))
        # print('middle coupon: {:,} ({})'.format(self.coupon, self.middle_tax))
        # print('last coupon: {:,} ({})'.format(self.last_coupon, self.last_tax))
        if self.coupon_days[0]:
            print('coupon {} ({:,}) - [{:,}] {:,}'.format(str(self.coupon_days[0])[:10], self.coupon, self.first_tax_base, self.first_tax))
        if len(self.coupon_days) >= 3:
            for coupon_date in self.coupon_days[1:-1]:
                print('coupon {} ({:,}) - [{:,}] {:,}'.format(str(coupon_date)[:10], self.coupon, self.middle_tax_base, self.middle_tax))
        if len(self.coupon_days) >= 2:
            print('coupon {} ({:,}) - [{:,}] {:,}'.format(str(self.coupon_days[-1])[:10], self.last_coupon, self.last_tax_base, self.last_tax))
        print('interest income: {:,}'.format(self.interest_income))
        print('capital income: {:,}'.format(self.capital_income))
        print('total income: {:,}'.format(self.total_income))
        print('tax: {:,}'.format(self.tax))
        print('profit: {:,}'.format(self.profit))
        print('profit rate: {:,.3f}%'.format(self.profit_rate))
        print('\033[096mprofit rate(annual): {:,.3f}%\033[0m'.format(int(self.profit_rate_annual * 1000) / 1000))
        print('\033[096mprofit rate(bank(A)): {:,.3f}%\033[0m'.format(int(self.profit_rate_bank * 1000) / 1000))
        print('profit rate(CAGR): {:,.3f}%'.format(self.CAGR))
        print('profit rate(bank(C)): {:,.3f}%'.format(self.CAGR_bank))


# Bond information
quick_item = BondItem()
quick_item.given_price = 8897
quick_item.coupon_rate = 1
quick_item.face_value = 10000
quick_item.payment_cycle = 12
quick_item.amount = 100
quick_item.given_discount_rate = 10
quick_item.compound_interest = True
quick_item.issue_date = '20221031'
quick_item.outset_date = ''
quick_item.maturity_date = '20271031'

item = BondItem()
item.set(b001)

# bond = Bond(quick_item)
bond = Bond(item)

# bond.analyze_price()
bond.analyze_discount_rate()

# Simple calculation
coupon = 0
future_value = 10510
current_value = 10000
discount_rate = 10
remaining_days = 365 * 5
frequency = 1

# dcv = bond.get_dcv_theoretical(future_value, discount_rate, remaining_days, frequency)
# dcv = bond.get_dcv_conventional(future_value, discount_rate, remaining_days, frequency)
# print(dcv)

# price_T = bond.calculate_theoretical_price(coupon, future_value, discount_rate, remaining_days, frequency)
# price_C = bond.calculate_conventional_price(coupon, future_value, discount_rate, remaining_days, frequency)
# price_W = bond.calculate_wook_price(coupon, future_value, discount_rate, remaining_days, frequency)
# discount_rate_T = bond.calculate_theoretical_discount_rate(current_value, coupon, future_value, remaining_days, frequency)
# discount_rate_C = bond.calculate_conventional_discount_rate(current_value, coupon, future_value, remaining_days, frequency)
# discount_rate_W = bond.calculate_wook_discount_rate(current_value, coupon, future_value, remaining_days, frequency)
# print('price(T)', price_T)
# print('price(C)', price_C)
# print('price(W)', price_W)
# print('Discount rate(T)', discount_rate_T)
# print('Discount rate(C)', discount_rate_C)
# print('Discount rate(W)', discount_rate_W)