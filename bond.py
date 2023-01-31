from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from compound_simple_items import *
from compound_items import *
from coupon_items import *
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
        self.compound_interest_number = item['compound interest number']
        self.simple_interest_number = item['simple interest number']

class Bond:
    def __init__(self, item):
        self.last_coupon = 0
        self.last_untreated_coupon = 0
        self.last_treated_coupon = 0
        self.untreated_coupon = 0
        self.treated_coupon = 0
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
        self.discount_term_number = 0
        self.discount_remainder_days = 0

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
        self.remaining_days = self.get_remaining_days()
        self.remaining_delta = relativedelta(self.maturity_date, self.outset_date)
        self.coupon_period = 365 / self.frequency
        self.term = relativedelta(months=item.payment_cycle)
        self.term_number = self.get_term_number()
        self.coupon_number = self.get_coupon_number()
        self.coupon_days = self.get_coupon_days()
        self.previous_coupon_date = self.get_previous_coupon_date()
        self.before_last_coupon_date = self.get_before_last_coupon_date()
        self.first_coupon_date = self.coupon_days[0]
        self.is_authentic_maturity = self.check_authentic_maturity()
        self.remainder_days = self.get_remainder_days()
        self.post_remainder = self.get_post_remainder()
        self.coupon = self.get_coupon()
        self.interest_income = self.get_interest_income()
        self.tax = self.get_tax()

    def get_term_number_deprecated(self):
        if self.type == 'coupon':
            remaining_months = self.remaining_delta.years * 12 + self.remaining_delta.months + self.remaining_delta.days / 31
            term_number = math.ceil(remaining_months / self.payment_cycle - 1)
        else:
            remaining_months = self.remaining_delta.years * 12 + self.remaining_delta.months
            term_number = int(remaining_months / self.payment_cycle)
        return term_number

    def get_term_number(self):
        if self.type == 'coupon':
            remaining_months = self.remaining_delta.years * 12 + self.remaining_delta.months + self.remaining_delta.days / 31
            term_number = math.ceil(remaining_months / self.payment_cycle - 1)
        else:
            remaining_months = self.remaining_delta.years * 12 + self.remaining_delta.months
            term_number = int(remaining_months / self.payment_cycle)
        return term_number

    def get_coupon_number(self):
        coupon_number = 0
        if self.type == 'coupon':
            coupon_number = self.term_number + 1
        elif self.type == 'compound':
            coupon_number = 1
        elif self.type == 'compound-simple':
            coupon_number = 1
        elif self.type == 'discount':
            coupon_number = 0
        return coupon_number

    def get_remaining_days(self):
        day_span_date = self.maturity_date - self.outset_date
        day_span = day_span_date.days
        return day_span

    def get_remainder_days(self):
        if self.type == 'coupon':
            remainder_period = self.first_coupon_date - self.outset_date
        else:
            virtual_coupon_date = self.first_coupon_date - self.term_number * relativedelta(months=self.payment_cycle)
            remainder_period = virtual_coupon_date - self.outset_date
        remainder_days = remainder_period.days
        return remainder_days

    def get_post_remainder(self):
        if self.type == 'coupon':
            if self.coupon_number > 1:
                if self.is_authentic_maturity:
                    post_remainder = 365 / self.frequency
                else:
                    post_remainder = (self.maturity_date - self.before_last_coupon_date).days
            else:
                post_remainder = (self.maturity_date - self.outset_date).days
        else:
            post_remainder = (self.maturity_date - self.issue_date).days
        return post_remainder

    def get_post_remainder_deprecated(self):
        if self.type == 'coupon':
            post_remainder = (self.maturity_date - self.before_last_coupon_date).days
        else:
            post_remainder = (self.maturity_date - self.issue_date).days
        return post_remainder

    def get_prepaid_count(self, current_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        current_issue_delta = relativedelta(current_date, self.issue_date)
        current_issue_months = current_issue_delta.years * 12 + current_issue_delta.months
        prepaid_count = current_issue_months // payment_cycle
        return prepaid_count

    def get_previous_coupon_date(self):
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(self.outset_date)
            previous_coupon_date = self.issue_date + self.term * prepaid_count
        else:
            previous_coupon_date = self.issue_date
        return previous_coupon_date

    def get_before_last_coupon_date(self):
        delta = relativedelta(self.maturity_date, self.issue_date)
        delta_months = delta.years * 12 + delta.months
        coupon_count = math.ceil(delta_months / self.payment_cycle)
        before_last_coupon_date = self.issue_date + (coupon_count - 1) * self.term
        return before_last_coupon_date

    def check_authentic_maturity(self):
        delta = relativedelta(self.maturity_date, self.issue_date)
        months = delta.years * 12 + delta.months
        remainder = months % self.payment_cycle + delta.days
        authentic_maturity = False if remainder else True
        return authentic_maturity

    def get_coupon_days(self):
        coupon_days = list()
        prepaid_count = self.get_prepaid_count(self.outset_date)
        term_number = self.term_number if self.type == 'coupon' else 0
        for coupon_index in range(term_number):
            coupon_day = self.issue_date + self.term * (prepaid_count + coupon_index + 1)
            coupon_days.append(coupon_day)
        coupon_days.append(self.maturity_date)
        return coupon_days

    def get_coupon_deprecated(self):
        coupon = 0
        if self.type == 'coupon':
            interest = self.face_value * (self.coupon_rate / 100) / self.frequency
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            coupon = int(self.untreated_coupon)
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.maturity_date)
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            # coupon = self.treated_coupon #국민주택22-10, 신한투자증권
            coupon = int(self.untreated_coupon) if self.frequency == 1 else self.treated_coupon
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            compound_interest = self.get_interest(10000, self.issue_date, transition_date)
            simple_interest = 10000 * (self.coupon_rate / 100) * self.simple_interest_number
            self.untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount
            coupon = int(self.untreated_coupon)
        return coupon

    def get_coupon(self):
        coupon = 0
        if self.type == 'coupon':
            annual_interest = self.face_value * (self.coupon_rate / 100)
            term_interest = annual_interest / self.frequency
            self.untreated_coupon = round(term_interest * self.amount, 6)
            self.treated_coupon = int(term_interest) * self.amount
            coupon = int(self.untreated_coupon)
            last_period = self.maturity_date - self.before_last_coupon_date
            if self.is_authentic_maturity:
                self.last_untreated_coupon = self.untreated_coupon
                self.last_treated_coupon = self.treated_coupon
                self.last_coupon = int(self.untreated_coupon)
            else:
                self.last_untreated_coupon = annual_interest * (last_period.days / 365) * self.amount
                self.last_treated_coupon = int(annual_interest * (last_period.days / 365)) * self.amount
                self.last_coupon = int(self.last_untreated_coupon)
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.maturity_date)
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            # coupon = self.treated_coupon #국민주택22-10, 신한투자증권
            coupon = int(self.untreated_coupon) if self.frequency == 1 else self.treated_coupon
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            compound_interest = self.get_interest(10000, self.issue_date, transition_date)
            simple_interest = 10000 * (self.coupon_rate / 100) * self.simple_interest_number
            self.untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount
            coupon = int(self.untreated_coupon)
        return coupon

    def get_interest_income(self):
        if self.type == 'coupon':
            interest_income = self.coupon * (self.coupon_number - 1) + self.last_coupon
        else:
            interest_income = self.coupon
        return interest_income

    def get_interest_income_deprecated(self):
        if self.type == 'coupon':
            before_last_coupon_date = self.coupon_days[-2] if self.coupon_number >= 2 else self.previous_coupon_date
            last_coupon_period = relativedelta(self.maturity_date, before_last_coupon_date)
            payment_cycle = relativedelta(months=self.payment_cycle)
            if last_coupon_period == payment_cycle:
                self.last_coupon = self.coupon
                self.last_untreated_coupon = self.untreated_coupon
            elif before_last_coupon_date.day == 28 and self.maturity_date.day == 29:
                self.last_coupon = self.coupon
                self.last_untreated_coupon = self.untreated_coupon
            else:
                whole_coupon = self.maturity_value * (self.coupon_rate / 100)
                last_period = self.maturity_date - before_last_coupon_date
                self.last_untreated_coupon = whole_coupon * (last_period.days / 365)
                self.last_coupon = int(whole_coupon * (last_period.days / 365))
            interest_income = self.coupon * (self.coupon_number - 1) + self.last_coupon
        else:
            interest_income = self.coupon
        return interest_income

    def get_tax(self):
        tax = 0
        if self.type == 'coupon':
            # coupon = (self.maturity_value / self.frequency) * (self.coupon_rate / 100)
            # first_coupon_date = self.coupon_days[0]
            # first_period = first_coupon_date - self.previous_coupon_date
            # first_imposing_days = (first_coupon_date - self.outset_date).days
            # first_tax_base = round(coupon * (first_imposing_days / first_period.days)) #삼성증권, 한국투자증권
            # # first_tax_base = int(self.coupon * (first_imposing_days / first_period.days)) #키움증권

            first_period = self.coupon_days[0] - self.previous_coupon_date
            deduction_days = (self.outset_date - self.previous_coupon_date).days
            first_coupon_deduction = int(self.untreated_coupon * (deduction_days / first_period.days))
            first_tax_base = int(self.untreated_coupon - first_coupon_deduction)
            self.first_tax_base = first_tax_base
            self.first_tax = self.calculate_tax(first_tax_base)
            self.middle_tax_base = self.coupon
            self.middle_tax = self.calculate_tax(self.untreated_coupon) if self.coupon_number >= 3 else 0
            self.last_tax_base = self.last_coupon
            self.last_tax = self.calculate_tax(self.last_coupon) if self.coupon_number >= 2 else 0
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        elif self.type == 'compound':
            deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
            deduction = int(deduction_unit * self.amount) #삼성증권, 키움증권
            # deduction = deduction_unit * self.amount #신한투자증권
            tax_base = int(self.coupon - deduction)
            self.first_tax_base = tax_base
            self.first_tax = self.calculate_tax(tax_base)
            tax = self.first_tax
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            if self.outset_date < transition_date:
                deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
                deduction = int(deduction_unit * self.amount)
            else:
                compound_deduction_unit = self.get_interest(10000, self.issue_date, transition_date)
                # compound_deduction = int(compound_deduction_unit * self.amount)
                compound_deduction = compound_deduction_unit * self.amount #키움증권, 삼성증권
                simple_deduction_period = self.outset_date - transition_date
                simple_deduction_days = simple_deduction_period.days
                simple_deduction = int(10000 * (self.coupon_rate / 100) * self.amount * (simple_deduction_days / 365))
                deduction = compound_deduction + simple_deduction
            tax_base = int(self.coupon - deduction)
            self.first_tax_base = tax_base
            self.first_tax = self.calculate_tax(tax_base)
            tax = self.first_tax
        return tax

    def calculate_tax(self, tax_base):
        income_tax = int(tax_base * 0.14 / 10) * 10
        residence_tax = int(income_tax * 0.1 / 10) * 10
        total_tax = income_tax + residence_tax
        return total_tax

    def get_CAGR(self, current_value, future_value, elapsed_days):
        CAGR = ((future_value / current_value) ** (1 / (elapsed_days / 365))) - 1
        return CAGR

    def get_fv_theoretical(self, principal, interest_rate, remaining_days, frequency=None, term=None):
        frequency = frequency if frequency else self.frequency
        interest_rate /= 100
        term = 365 / frequency if not term else term

        fv = principal * ((1 + (interest_rate / frequency)) ** (remaining_days / term))

        return fv

    def get_fv_conventional(self, principal, interest_rate, term_number, remainder_days=None, frequency=None):
        f = frequency if frequency else self.frequency
        r = interest_rate / 100
        d = remainder_days if remainder_days is not None else self.remainder_days

        fv = principal * (((1 + (r / f)) ** term_number) * (1 + (r * (d / 365))))

        return fv

    def get_term_days(self, start_date, end_date, payment_cycle):
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        term_end_date = start_date + term_number * relativedelta(months=payment_cycle)
        remainder_days = (end_date - term_end_date).days
        return term_number, remainder_days

    def get_discount_term_days_deprecated(self, start_date, end_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        prepaid_count = self.get_prepaid_count(start_date, payment_cycle)
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        term_start_date = self.issue_date + (prepaid_count + 1) * relativedelta(months=payment_cycle)
        remainder_days = (term_start_date - start_date).days
        return term_number, remainder_days

    def get_discount_term_days(self, start_date, end_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        prepaid_count = self.get_prepaid_count(start_date, payment_cycle)
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        term_start_date = self.issue_date + (prepaid_count + 1) * relativedelta(months=payment_cycle)
        remainder_days = (term_start_date - start_date).days if term_start_date < self.maturity_date else 0
        return term_number, remainder_days

    def get_term(self, start_date, term_number):
        payment_delta = relativedelta(months=self.payment_cycle)
        previous_term_date = start_date + term_number * payment_delta
        next_term_date = previous_term_date + payment_delta
        term = (next_term_date - previous_term_date).days
        return term

    def get_interest(self, principal, start_date=None, end_date=None, interest_rate=None, payment_cycle=None):
        start_date = start_date if start_date else self.issue_date
        end_date = end_date if end_date else self.maturity_date
        interest_rate = interest_rate if interest_rate else self.coupon_rate
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        frequency = 12 / payment_cycle

        term_number, remainder_days = self.get_term_days(start_date, end_date, payment_cycle)
        term = self.get_term(start_date, term_number)
        term_days = term * term_number
        remaining_days = term_days + remainder_days
        principal_interest = self.get_fv_theoretical(principal, interest_rate, remaining_days, frequency, term)
        interest = principal_interest - principal
        return interest

    def get_interest_conventional(self, principal, start_date=None, end_date=None, interest_rate=None, payment_cycle=None):
        start_date = start_date if start_date else self.issue_date
        end_date = end_date if end_date else self.maturity_date
        interest_rate = interest_rate if interest_rate else self.coupon_rate
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        frequency = 12 / payment_cycle

        term_number, remainder_days = self.get_term_days(start_date, end_date, payment_cycle)
        principal_interest = self.get_fv_conventional(principal, interest_rate, term_number, remainder_days, frequency)
        interest = principal_interest - principal
        return interest

    def get_dcv(self, future_value, start_date, end_date=None, discount_rate=None, payment_cycle=None):
        start_date = start_date if start_date else self.issue_date
        end_date = end_date if end_date else self.maturity_date
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        frequency = 12 / payment_cycle

        term_number, remainder_days = self.get_term_days(start_date, end_date, payment_cycle)
        term = self.get_term(start_date, term_number)
        term_days = term * term_number
        remaining_days = term_days + remainder_days
        dcv = self.get_dcv_theoretical(future_value, discount_rate, remaining_days, frequency, term)
        return dcv

    def get_dcv_theoretical(self, future_value, discount_rate=None, remaining_days=None, frequency=None, term=None):
        remaining_days = remaining_days if remaining_days is not None else self.remaining_days
        r = discount_rate if discount_rate is not None else self.given_discount_rate
        f = frequency if frequency else self.frequency
        term = 365 / f if not term else term
        r /= 100

        dcv = future_value / \
              ((1 + (r / f)) ** (remaining_days / term))

        return dcv

    def get_dcv_conventional_deprecated(self, future_value, discount_rate, term_number, remainder_days=None, frequency=None, term=None):
        f = frequency if frequency else self.frequency
        r = discount_rate / 100
        d = remainder_days if remainder_days is not None else self.remainder_days
        term = term if term else 365

        dcv = future_value / \
              (((1 + r / f) ** term_number) * (1 + (r / f) * (d / term)))

        return dcv

    def get_dcv_conventional(self, future_value, discount_rate, term_number, remainder_days=None, frequency=None, term=None, post_remainder=None):
        f = frequency if frequency else self.frequency
        r = discount_rate / 100
        d = remainder_days if remainder_days is not None else self.remainder_days
        term = term if term else 365
        R = post_remainder if post_remainder else (365 / f)
        term_number -= 1

        dcv = future_value / \
              ((1 + (r / f) * (d / term)) * ((1 + r / f) ** term_number) * (1 + (r * (R / 365))))

        return dcv

    def get_dcv_post(self, future_value, discount_rate, term_number, remainder_days, term, post_remainder, frequency=None):
        f = frequency if frequency else self.frequency
        r = discount_rate / 100
        d = remainder_days
        term_number -= 1
        term = term if term else 365
        R = post_remainder if post_remainder else 0

        dcv = future_value / \
              (((1 + r / f) ** term_number) * (1 + (r / f) * (d / term)) * (1 + (r * (R / 365))))

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
        if self.type == 'coupon':
            term = (self.coupon_days[0] - self.previous_coupon_date).days
            for coupon_date in self.coupon_days[:-1]:
                coupon_term, coupon_remainder = self.get_discount_term_days(self.outset_date, coupon_date)
                price += self.get_dcv_conventional(self.untreated_coupon, discount_rate, coupon_term, coupon_remainder, self.frequency, term)
            term_number, remainder_days = self.get_discount_term_days(self.outset_date, self.maturity_date)

            # post_remainder = self.post_remainder if not self.is_authentic_maturity else None
            price += self.get_dcv_conventional(self.last_untreated_coupon, discount_rate, term_number, remainder_days, self.frequency, term, self.post_remainder)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, term_number, remainder_days, self.frequency, term, self.post_remainder)

            # post_remainder = self.post_remainder if not self.is_authentic_maturity else None
            # price += self.get_dcv_conventional(self.last_untreated_coupon, discount_rate, term_number, remainder_days, self.frequency, term, post_remainder)
            # price += self.get_dcv_conventional(self.maturity_value, discount_rate, term_number, remainder_days, self.frequency, term, post_remainder)
        elif self.type == 'compound':
            term_number, remainder_days = self.get_discount_term_days(self.outset_date, self.maturity_date, 12)
            price += self.get_dcv_conventional(self.treated_coupon, discount_rate, term_number, remainder_days, 1)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, term_number, remainder_days, 1)
        elif self.type == 'compound-simple':
            term_number, remainder_days = self.get_discount_term_days(self.outset_date, self.maturity_date, 12)
            price += self.get_dcv_conventional(self.treated_coupon, discount_rate, term_number, remainder_days, 1)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, term_number, remainder_days, 1)
        return price

    def get_price_conventional_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        term_number, remainder_days = self.get_discount_term_days(self.outset_date, self.maturity_date)
        term = (self.coupon_days[0] - self.previous_coupon_date).days

        price = 0
        # if self.type == 'coupon':

        # First term
        first_income = self.untreated_coupon - self.first_tax if self.coupon_number > 1 else 0
        price += self.get_dcv_conventional(first_income, discount_rate, 0, remainder_days, self.frequency, term)

        # Mid term
        for coupon_date in self.coupon_days[1:-1]:
            middle_income = self.untreated_coupon - self.middle_tax
            coupon_term, coupon_remainder = self.get_discount_term_days(self.outset_date, coupon_date)
            price += self.get_dcv_conventional(middle_income, discount_rate, coupon_term, coupon_remainder, self.frequency, term)

        # Last term
        # post_remainder = self.post_remainder if not self.is_authentic_maturity else None
        # price += self.get_dcv_conventional(self.last_untreated_coupon, discount_rate, term_number, remainder_days,
        #                                    self.frequency, term, post_remainder)

        last_income = self.last_untreated_coupon - self.last_tax
        price += self.get_dcv_conventional(last_income, discount_rate, term_number, remainder_days, self.frequency, term)

        # Maturity value
        price += self.get_dcv_conventional(self.maturity_value, discount_rate, self.term_number, remainder_days, self.frequency, term)
        return price

    def get_price_wook(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_date in self.coupon_days:
            coupon_term, coupon_remainder = self.get_discount_term_days(self.outset_date, coupon_date, 12)
            remaining_days = coupon_term * 365 + coupon_remainder
            price += self.get_dcv_theoretical(self.untreated_coupon, discount_rate, remaining_days, 1)
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
            last_income = self.last_treated_coupon - self.last_tax
            price += self.get_dcv_theoretical(last_income, discount_rate, remaining_days, 1)

        # Maturity value
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, self.remaining_days, 1)
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
        return discount_rate

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
        self.discount_rate = int(self.get_discount_rate() * 1000) / 1000
        self.discount_rate_tax = int(self.get_discount_rate_tax() * 1000) / 1000
        self.discount_rate_tax_bank = round(self.discount_rate_tax / 0.846, 3)
        self.discount_rate_wook = int(self.get_discount_rate_wook() * 1000) / 1000
        self.discount_rate_wook_tax = int(self.get_discount_rate_wook_tax() * 1000) / 1000
        self.discount_rate_wook_tax_bank = round(self.discount_rate_wook_tax / 0.846, 3)

        print('=================================================')
        print('      Discount Rate Analysis (price: {:,})      '.format(self.given_price))
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
        self.profit_rate_annual = int(self.profit_rate / (self.remaining_days / 365) * 1000) / 1000
        self.profit_rate_bank = int(self.profit_rate / (self.remaining_days / 365) / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(self.price * self.amount, self.price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

        print('name:', self.name)
        print('type:', self.type, '({:,} / {:,})'.format(round(self.untreated_coupon, 5), self.treated_coupon))
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
        if self.coupon_days[0]:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.format(str(self.coupon_days[0])[:10], self.coupon, self.first_tax_base, self.first_tax))
        for coupon_date in self.coupon_days[1:-1]:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.format(str(coupon_date)[:10], self.coupon, self.middle_tax_base, self.middle_tax))
        if len(self.coupon_days) >= 2:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.format(str(self.coupon_days[-1])[:10], self.last_coupon, self.last_tax_base, self.last_tax))
        print('interest income: {:,}'.format(self.interest_income))
        print('capital income: {:,}'.format(self.capital_income))
        print('total income: {:,}'.format(self.total_income))
        print('tax: {:,}'.format(self.tax))
        print('profit: {:,}'.format(self.profit))
        print('profit rate: {:,.3f}%'.format(self.profit_rate))
        print('\033[096mprofit rate(annual): {:,.3f}%\033[0m'.format(self.profit_rate_annual))
        print('\033[096mprofit rate(bank(A)): {:,.3f}%\033[0m'.format(self.profit_rate_bank))
        print('profit rate(CAGR): {:,.3f}%'.format(self.CAGR))
        print('profit rate(bank(C)): {:,.3f}%'.format(self.CAGR_bank))


# Bond information
quick_item = BondItem()
quick_item.name = 'Quick analysis'
quick_item.type = 'coupon'
quick_item.given_price = 9801.1
quick_item.coupon_rate = 4.4
quick_item.face_value = 10000
quick_item.payment_cycle = 3
quick_item.amount = 100
quick_item.given_discount_rate = 10
quick_item.issue_date = '20211008'
quick_item.outset_date = ''
quick_item.maturity_date = '20231006'

item = BondItem()
item.set(c036)
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

# d = bond.outset_date
# print(d)
#
# day1 = datetime.strptime('20221013', '%Y%m%d')
# day2 = datetime.strptime('20230112', '%Y%m%d')
# day2 = bond.outset_date
# days = (day2 - day1).days
# delta = relativedelta(day2, day1)
# print(days)
# print(delta)