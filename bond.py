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
        self.given_sale_price = 0
        self.given_sale_discount_rate = 0.0
        self.coupon_rate = 0.0
        self.face_value = 10000
        self.payment_cycle = 12
        self.amount = 0
        self.issue_date = ''
        self.maturity_date = ''
        self.outset_date = ''
        self.sale_date = ''
        self.compound_interest_number = 0
        self.simple_interest_number = 0

    def set(self, item):
        self.name = item['name']
        self.type = item['type']
        self.given_price = item['price']
        self.given_discount_rate = item['discount rate']
        self.given_sale_price = item['sale price']
        self.given_sale_discount_rate = item['sale discount rate']
        self.coupon_rate = item['coupon rate']
        self.face_value = item['face value']
        self.payment_cycle = item['payment cycle']
        self.amount = item['amount']
        self.issue_date = item['issue date']
        self.maturity_date = item['maturity date']
        self.outset_date = item['outset date']
        self.sale_date = item['sale date']
        self.compound_interest_number = item['compound interest number']
        self.simple_interest_number = item['simple interest number']

class Bond:
    def __init__(self, item):
        self.untreated_coupon = 0
        self.treated_coupon = 0
        self.maturity_untreated_coupon = 0
        self.maturity_treated_coupon = 0
        self.last_coupon = 0
        self.outset_interest = 0
        self.sale_interest = 0
        self.treated_sale_interest = 0
        self.outset_valuation = 0
        self.sale_valuation = 0
        self.sale_assessment = 0
        self.valuation_profit = 0
        self.valuation_profit_actual = 0
        self.coupon_profit = 0
        self.coupon_profit_actual = 0
        self.interest_income = 0
        self.capital_income = 0
        self.capital_income_actual = 0
        self.capital_income_outset = 0
        self.capital_income_sale = 0
        self.capital_difference_outset = 0
        self.capital_difference_sale = 0
        self.capital_income_exhibit = 0
        self.total_income = 0
        self.total_income_actual = 0
        self.profit = 0.0
        self.profit_rate = 0.0
        self.profit_rate_annual = 0.0
        self.profit_rate_annual_pretax = 0.0
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
        self.price_maturity = 0
        self.price_tax = 0
        self.price_theoretical = 0
        self.price_theoretical_tax = 0
        self.price_wook = 0
        self.price_wook_tax = 0
        self.price_wook_tax_bank = 0
        self.discount_rate = 0.0
        self.discount_rate_maturity = 0.0
        self.discount_rate_tax = 0.0
        self.discount_rate_tax_bank = 0.0
        self.discount_rate_theoretical = 0
        self.discount_rate_theoretical_tax = 0
        self.discount_rate_theoretical_tax_bank = 0
        self.discount_rate_wook = 0.0
        self.discount_rate_wook_tax = 0.0
        self.discount_rate_wook_tax_bank = 0.0
        self.sale_price = 0
        self.sale_discount_rate = 0.0
        self.price_is_given = True

        self.duration = 0.0
        self.modified_duration = 0.0
        self.dollar_duration = 0.0
        self.convexity = 0.0
        self.dv01 = 0.0
        self.positive_delta_price = 0
        self.negative_delta_price = 0

        self.name = item.name
        self.type = item.type
        self.payment_cycle = item.payment_cycle
        self.frequency = int(12 / item.payment_cycle)
        self.compound_interest_number = item.compound_interest_number
        self.simple_interest_number = item.simple_interest_number
        self.coupon_rate = item.coupon_rate
        self.given_price = item.given_price
        self.given_sale_price = item.given_sale_price
        self.given_sale_discount_rate = item.given_sale_discount_rate

        self.face_value = item.face_value
        self.maturity_value = item.face_value * item.amount
        self.purchase_value = item.given_price * item.amount
        self.amount = item.amount
        self.given_discount_rate = item.given_discount_rate
        self.issue_date = datetime.strptime(item.issue_date, '%Y%m%d')
        self.maturity_date = datetime.strptime(item.maturity_date, '%Y%m%d')
        self.outset_date = datetime.strptime(item.outset_date, '%Y%m%d') if item.outset_date else datetime.combine(date.today(), time.min)
        self.sale_date = datetime.strptime(item.sale_date, '%Y%m%d') if item.sale_date else self.maturity_date
        self.remaining_days = (self.sale_date - self.outset_date).days
        self.remaining_delta = relativedelta(self.sale_date, self.outset_date)
        self.year_remainder = ((self.sale_date - relativedelta(years=self.remaining_delta.years)) - self.outset_date).days
        self.maturity = True if self.sale_date == self.maturity_date else False
        self.term = relativedelta(months=item.payment_cycle)
        self.term_number = self.get_term_number(self.sale_date)
        self.coupon_number = self.get_coupon_number(self.sale_date)
        self.payment_number = self.get_payment_number()
        self.maturity_coupon_number = self.get_coupon_number(self.maturity_date)
        self.unpaid_coupon_number = self.get_coupon_number(self.maturity_date, self.sale_date)
        self.coupon_days = self.get_coupon_days(self.coupon_number, self.sale_date)
        self.maturity_coupon_days = self.get_coupon_days(self.maturity_coupon_number, self.maturity_date)
        self.unpaid_coupon_days = self.get_coupon_days(self.unpaid_coupon_number, self.maturity_date, self.sale_date)
        self.payment_days = self.get_payment_days()
        self.previous_coupon_date = self.get_previous_coupon_date()
        self.outset_interest_start_date = self.get_interest_start_date(self.outset_date)
        self.sale_interest_start_date = self.get_interest_start_date(self.sale_date)
        self.maturity_interest_start_date = self.get_interest_start_date(self.maturity_date)
        self.maturity_sale_reference_date = self.get_interest_start_date(self.maturity_date - relativedelta(days=1))
        self.outset_fraction = self.get_coupon_fraction(self.outset_date)
        self.sale_fraction = self.get_coupon_fraction(self.sale_date)
        self.maturity_fraction = self.get_coupon_fraction(self.maturity_date)
        self.outset_date_is_authentic = self.check_authenticity(self.outset_date)
        self.sale_date_is_authentic = self.check_authenticity(self.sale_date)
        self.maturity_date_is_authentic = self.check_authenticity(self.maturity_date)
        self.set_values()
        self.tax = self.get_tax()

    def get_term_number(self, end_date, start_date=None):
        start_date = start_date if start_date else self.outset_date
        if self.type == 'coupon':
            term_start_count = self.get_next_pay_count(start_date)
            term_end_count = self.get_prepaid_count(end_date)
            term_number = term_end_count - term_start_count
        else:
            remaining_delta = relativedelta(end_date, start_date)
            remaining_months = remaining_delta.years * 12 + remaining_delta.months
            term_number = remaining_months // self.payment_cycle
        return term_number

    def get_coupon_number(self, end_date, start_date=None):
        start_date = start_date if start_date else self.outset_date
        coupon_number = 0
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(start_date)
            next_pay_count = self.get_next_pay_count(end_date)
            coupon_number = next_pay_count - prepaid_count
        elif self.type == 'compound':
            coupon_number = 1
        elif self.type == 'compound-simple':
            coupon_number = 1
        elif self.type == 'discount':
            coupon_number = 0
        return coupon_number

    def get_payment_number(self):
        payment_number = 0
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(self.outset_date)
            last_count = self.get_prepaid_count(self.sale_date)
            payment_number = last_count - prepaid_count
        elif self.type == 'compound':
            payment_number = 1 if self.maturity else 0
        elif self.type == 'compound-simple':
            payment_number = 1 if self.maturity else 0
        elif self.type == 'discount':
            payment_number = 0
        return payment_number

    def get_prepaid_count(self, current_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        current_issue_delta = relativedelta(current_date, self.issue_date)
        current_issue_months = current_issue_delta.years * 12 + current_issue_delta.months
        prepaid_count = current_issue_months // payment_cycle
        return prepaid_count

    def get_raw_prepaid_count(self, current_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        current_issue_delta = relativedelta(current_date, self.issue_date)
        current_issue_months = current_issue_delta.years * 12 + current_issue_delta.months + current_issue_delta.days / 31
        prepaid_count = current_issue_months / payment_cycle
        return prepaid_count

    def get_next_pay_count(self, current_date, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        current_issue_delta = relativedelta(current_date, self.issue_date)
        current_issue_months = current_issue_delta.years * 12 + current_issue_delta.months + current_issue_delta.days / 31
        next_pay_count = math.ceil(current_issue_months / payment_cycle)
        return next_pay_count

    def get_previous_coupon_date(self):
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(self.outset_date)
            previous_coupon_date = self.issue_date + self.term * prepaid_count
        else:
            previous_coupon_date = self.issue_date
        return previous_coupon_date

    def get_interest_start_date(self, reference_date):
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(reference_date)
            interest_start_date = self.issue_date + prepaid_count * self.term
        else:
            interest_start_date = self.issue_date
        return interest_start_date

    def get_coupon_fraction(self, reference_date):
        prepaid_count = self.get_prepaid_count(reference_date)
        term_start_date = self.issue_date + prepaid_count * self.term
        term_end_date = self.issue_date + (prepaid_count + 1) * self.term
        term = (term_end_date - term_start_date).days
        coupon_period = (reference_date - term_start_date).days

        if term_start_date == reference_date:
            coupon_fraction = (1 / self.frequency)
        elif term_start_date == self.maturity_interest_start_date:
            coupon_fraction = coupon_period / 365
        else:
            coupon_fraction = (1 / self.frequency) * coupon_period / term

        return coupon_fraction

    def get_year_fraction(self, start_date, end_date):
        remaining_delta = relativedelta(end_date, start_date)
        year_end_date = start_date + relativedelta(years=remaining_delta.years)
        term_end_date = year_end_date + relativedelta(years=1)
        term = (term_end_date - year_end_date).days
        remaining_days = (end_date - year_end_date).days
        fraction = remaining_delta.years + remaining_days / term
        return fraction

    def check_authenticity(self, end_date):
        delta = relativedelta(end_date, self.issue_date)
        months = delta.years * 12 + delta.months
        remainder = months % self.payment_cycle + delta.days
        authenticity = False if remainder else True
        return authenticity

    def get_coupon_days(self, coupon_number, end_date, start_date=None):
        start_date = start_date if start_date else self.outset_date
        coupon_days = list()
        prepaid_count = self.get_prepaid_count(start_date)
        coupon_number = coupon_number if self.type == 'coupon' else 0
        for coupon_index in range(1, coupon_number):
            coupon_day = self.issue_date + self.term * (prepaid_count + coupon_index)
            coupon_days.append(coupon_day)
        coupon_days.append(end_date)
        return coupon_days

    def get_payment_days(self):
        payment_days = list()
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(self.outset_date)
            last_count = self.get_prepaid_count(self.sale_date)
            payment_number = last_count - prepaid_count
            for payment_index in range(payment_number):
                payment_day = self.issue_date + self.term * (prepaid_count + (payment_index + 1))
                payment_days.append(payment_day)
        else:
            if self.maturity:
                payment_days.append(self.maturity_date)
        return payment_days

    def set_values(self):
        if self.type == 'coupon':
            self.set_coupon_values()
        elif self.type == 'compound':
            self.set_compound_values()
        elif self.type == 'compound-simple':
            self.set_compound_simple_values()

    def set_coupon_values(self):
        annual_interest = self.face_value * (self.coupon_rate / 100)
        outset_interest = annual_interest * self.outset_fraction
        sale_interest = annual_interest * self.sale_fraction
        self.outset_interest = outset_interest if not self.outset_date_is_authentic else 0
        self.sale_interest = sale_interest if not self.sale_date_is_authentic else 0
        self.untreated_coupon = round(annual_interest / self.frequency * self.amount, 6)
        self.treated_coupon = int(annual_interest / self.frequency) * self.amount
        self.last_coupon = self.untreated_coupon if self.sale_date_is_authentic else self.sale_interest * self.amount
        self.maturity_untreated_coupon = annual_interest * self.maturity_fraction * self.amount
        self.maturity_treated_coupon = int(annual_interest * self.maturity_fraction) * self.amount
        self.coupon_profit = int(self.untreated_coupon) * self.term_number
        self.coupon_profit_actual = self.untreated_coupon * self.term_number
        self.outset_valuation = self.face_value + self.outset_interest
        self.sale_valuation = self.face_value + self.sale_interest
        self.sale_assessment = self.face_value + sale_interest if self.maturity else self.sale_valuation
        outset_value = outset_interest * self.amount
        sale_value = self.sale_interest * self.amount
        self.valuation_profit = (int(self.untreated_coupon) - int(outset_value)) + int(sale_value)
        self.valuation_profit_actual = (self.untreated_coupon - outset_value) + sale_value

    def set_compound_values(self):
        self.outset_interest = self.get_interest(self.face_value, self.issue_date, self.outset_date)
        sale_interest = self.get_interest(self.face_value, self.issue_date, self.sale_date)
        self.sale_interest = sale_interest
        self.treated_sale_interest = int(sale_interest) if self.maturity and self.payment_cycle != 12 else sale_interest
        maturity_interest = self.get_interest(self.face_value, self.issue_date, self.maturity_date)
        self.untreated_coupon = sale_interest * self.amount # treated_coupon 국민주택22-10, 신한투자증권
        self.treated_coupon = int(sale_interest) * self.amount
        self.last_coupon = self.untreated_coupon if self.sale_date_is_authentic else self.sale_interest * self.amount
        self.maturity_untreated_coupon = maturity_interest * self.amount
        self.maturity_treated_coupon = int(maturity_interest) * self.amount
        self.outset_valuation = self.face_value + self.outset_interest
        self.sale_valuation = self.face_value + self.sale_interest
        self.sale_assessment = self.face_value + self.sale_interest
        self.valuation_profit = int(self.treated_sale_interest * self.amount) - int(self.outset_interest * self.amount)
        self.valuation_profit_actual = sale_interest * self.amount - self.outset_interest * self.amount

    def set_compound_simple_values(self):
        transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
        outset_compound_interest = self.get_interest(self.face_value, self.issue_date, min(transition_date, self.outset_date))
        outset_simple_interest_number = self.get_simple_interest_number(transition_date, self.outset_date)
        outset_simple_interest = self.face_value * (self.coupon_rate / 100) * outset_simple_interest_number
        self.outset_interest = outset_compound_interest + outset_simple_interest
        sale_compound_interest = self.get_interest(self.face_value, self.issue_date, min(transition_date, self.sale_date))
        sale_simple_interest_number = self.get_simple_interest_number(transition_date, self.sale_date)
        sale_simple_interest = self.face_value * (self.coupon_rate / 100) * sale_simple_interest_number
        self.sale_interest = sale_compound_interest + sale_simple_interest
        maturity_compound_interest = self.get_interest(self.face_value, self.issue_date, transition_date)
        maturity_simple_interest = self.face_value * (self.coupon_rate / 100) * self.simple_interest_number
        self.untreated_coupon = self.sale_interest * self.amount
        self.treated_coupon = (int(sale_compound_interest) + int(sale_simple_interest)) * self.amount
        self.last_coupon = self.untreated_coupon
        self.maturity_untreated_coupon = (maturity_compound_interest + maturity_simple_interest) * self.amount
        self.maturity_treated_coupon = (int(maturity_compound_interest) + int(maturity_simple_interest)) * self.amount
        self.outset_valuation = self.face_value + self.outset_interest
        self.sale_valuation = self.face_value + self.sale_interest
        self.sale_assessment = self.face_value + self.sale_interest
        self.valuation_profit = int(self.sale_interest * self.amount) - int(self.outset_interest * self.amount)
        self.valuation_profit_actual = self.sale_interest * self.amount - self.outset_interest * self.amount

    def get_tax(self):
        tax = 0
        if self.type == 'coupon':
            if self.coupon_number >= 2:
                first_period = self.coupon_days[0] - self.previous_coupon_date
                deduction_days = (self.outset_date - self.previous_coupon_date).days
                first_coupon_deduction = int(self.untreated_coupon * (deduction_days / first_period.days))
                first_tax_base = int(self.untreated_coupon - first_coupon_deduction)
                self.first_tax_base = first_tax_base
                self.first_tax = self.calculate_tax(first_tax_base)
            if self.coupon_number >= 3:
                self.middle_tax_base = int(self.untreated_coupon)
                self.middle_tax = self.calculate_tax(self.untreated_coupon)
            last_term = True if self.coupon_number == 1 else False
            last_period = (self.sale_date - self.outset_interest_start_date).days
            deduction_days = (self.outset_date - self.outset_interest_start_date).days if last_term else 0
            last_coupon_deduction = int(self.last_coupon * (deduction_days / last_period)) if last_term else 0
            last_tax_base = int(round(self.last_coupon, 6) - last_coupon_deduction)
            self.last_tax_base = last_tax_base
            self.last_tax = self.calculate_tax(last_tax_base)
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        elif self.type == 'compound':
            tax_base = self.valuation_profit  #삼성증권, 키움증권
            # tax_base = int(self.untreated_coupon - deduction)  #신한투자증권
            self.last_tax_base = tax_base
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        elif self.type == 'compound-simple':
            tax_base = self.valuation_profit
            self.last_tax_base = int(tax_base)
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        return tax

    def get_simple_interest_number(self, start_date, end_date):
        one_year = relativedelta(years=1)
        reference_date = start_date
        simple_interest_number = 0
        while reference_date < end_date:
            next_year = reference_date + one_year
            simple_interest_period = (next_year - reference_date).days
            simple_interest_days = (min(next_year, end_date) - reference_date).days
            simple_interest_number += simple_interest_days / simple_interest_period
            reference_date += one_year
        return simple_interest_number

    def calculate_tax(self, tax_base):
        income_tax = int(tax_base * 0.14 / 10) * 10
        residence_tax = int(income_tax * 0.1 / 10) * 10
        total_tax = income_tax + residence_tax
        return total_tax

    def get_CAGR(self, current_value, future_value, elapsed_days):
        CAGR = ((future_value / current_value) ** (1 / (elapsed_days / 365))) - 1
        return CAGR

    def get_fv_theoretical(self, principal, interest_rate, remaining_days, frequency=None, term=None):
        f = frequency if frequency else self.frequency
        r = interest_rate / 100
        term = 365 / frequency if not term else term

        fv = principal * ((1 + (r / f)) ** (remaining_days / term))

        return fv

    def get_fv_conventional(self, principal, interest_rate, term_number, remainder_days, frequency=None):
        f = frequency if frequency else self.frequency
        r = interest_rate / 100
        d = remainder_days

        fv = principal * (((1 + (r / f)) ** term_number) * (1 + (r * (d / 365))))

        return fv

    def get_term_days(self, start_date, end_date, payment_cycle):
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        term_end_date = start_date + term_number * relativedelta(months=payment_cycle)
        remainder_days = (end_date - term_end_date).days
        if start_date.month == 2 and start_date.day == 28 and end_date.month == 2 and end_date.day == 29:
            remainder_days = 0

        return term_number, remainder_days

    def get_term(self, start_date, term_number, payment_cycle=None):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        payment_delta = relativedelta(months=payment_cycle)
        previous_term_date = start_date + term_number * payment_delta
        next_term_date = previous_term_date + payment_delta
        term = (next_term_date - previous_term_date).days
        return term

    def get_interest(self, principal, start_date=None, end_date=None, interest_rate=None, payment_cycle=None):
        start_date = start_date if start_date else self.issue_date
        end_date = end_date if end_date else self.sale_date
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
        end_date = end_date if end_date else self.sale_date
        interest_rate = interest_rate if interest_rate else self.coupon_rate
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        frequency = 12 / payment_cycle

        term_number, remainder_days = self.get_term_days(start_date, end_date, payment_cycle)
        principal_interest = self.get_fv_conventional(principal, interest_rate, term_number, remainder_days, frequency)
        interest = principal_interest - principal
        return interest

    def get_dcv_conventional(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset = outset_date if outset_date else self.outset_date
        payment = payment_date if payment_date else self.maturity_date
        cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / cycle

        pre_term, pre_remainder, TN, post_term, post_remainder = self.parse_terms(cycle, payment, outset)

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r * (post_remainder / 365))))

        return dcv

    def get_dcv_sale(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset = outset_date if outset_date else self.outset_date
        payment = payment_date if payment_date else self.maturity_date
        cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle

        pre_term, pre_remainder, TN, post_term, post_remainder = self.parse_terms(cycle, payment, outset, False)

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r * (post_remainder / 365))))

        return dcv

    def parse_terms(self, payment_cycle=None, payment_date=None, outset_date=None, correct_leap_year=False):
        term_delta = relativedelta(months=payment_cycle)
        one_day = relativedelta(days=1)

        outset_cycles = self.get_raw_prepaid_count(outset_date, payment_cycle)
        pre_term_count = int(outset_cycles)
        term_start_count = pre_term_count + 1
        payment_cycles = self.get_raw_prepaid_count(payment_date, payment_cycle)
        post_term_count = math.ceil(payment_cycles)
        term_end_count = int(payment_cycles)

        term_number = term_end_count - term_start_count
        TN = term_number if term_number > 0 else 0
        pre_term_date = self.issue_date + pre_term_count * term_delta
        term_start_date = self.issue_date + term_start_count * term_delta
        term_end_date = self.issue_date + term_end_count * term_delta
        post_term_date = self.issue_date + post_term_count * term_delta
        last_term = False if term_start_date <= term_end_date else True

        # Leap year correction
        if correct_leap_year:
            pre_term_is_leap_year = True if (term_start_date - pre_term_date).days == 366 else False
            pre_term_is_last_year = True if (term_end_date - term_start_date).days == 0 else False
            full_leap_year = True if (term_start_date - outset_date).days == 366 else False
            last_term_is_leap_year = True if (term_end_date - term_start_date).days == 366 else False
            full_year = True if (post_term_date - term_end_date).days == 0 else False
            if pre_term_is_leap_year and pre_term_is_last_year and not full_leap_year:
                pre_term_date = pre_term_date + one_day
            elif pre_term_is_leap_year and pre_term_is_last_year and full_leap_year:
                pre_term_date = pre_term_date - term_delta
                term_start_date = term_start_date - term_delta + one_day
                TN += 1
            elif last_term_is_leap_year and full_year:
                term_start_date += one_day

        pre_term = (term_start_date - pre_term_date).days
        pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        return pre_term, pre_remainder, TN, post_term, post_remainder

    def get_dcv_theoretical(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle

        pre_term, pre_remainder, TN, post_term, post_remainder = \
            self.parse_theoretical_terms(payment_cycle, payment_date, outset_date, False)

        dcv = future_value / \
              ((1 + (r / f)) ** ((pre_remainder / pre_term) + TN + (post_remainder / post_term)))

        return dcv

    def parse_theoretical_terms(self, payment_cycle=None, payment_date=None, outset_date=None, correct_leap_year=False):
        term_delta = relativedelta(months=payment_cycle)
        one_day = relativedelta(days=1)

        issue_outset_cycles = self.get_raw_prepaid_count(outset_date, payment_cycle)
        pre_term_start_count = int(issue_outset_cycles)
        term_start_count = pre_term_start_count + 1
        issue_payment_cycles = self.get_raw_prepaid_count(payment_date, payment_cycle)
        post_term_end_count = math.ceil(issue_payment_cycles)
        term_end_count = post_term_end_count - 1

        term_number = term_end_count - term_start_count
        TN = term_number if term_number > 0 else 0
        pre_term_date = self.issue_date + pre_term_start_count * term_delta
        term_start_date = self.issue_date + term_start_count * term_delta
        term_end_date = self.issue_date + term_end_count * term_delta
        post_term_date = self.issue_date + post_term_end_count * term_delta
        last_term = False if term_start_date <= term_end_date else True

        # Leap year correction
        if correct_leap_year:
            pre_term_is_leap_year = True if (term_start_date - pre_term_date).days == 366 else False
            pre_term_is_last_year = True if (term_end_date - term_start_date).days == 0 else False
            full_leap_year = True if (term_start_date - outset_date).days == 366 else False
            last_term_is_leap_year = True if (term_end_date - term_start_date).days == 366 else False
            full_year = True if (post_term_date - term_end_date).days == 0 else False
            if pre_term_is_leap_year and pre_term_is_last_year and not full_leap_year:
                pre_term_date = pre_term_date + one_day
            elif pre_term_is_leap_year and pre_term_is_last_year and full_leap_year:
                pre_term_date = pre_term_date - term_delta
                term_start_date = term_start_date - term_delta + one_day
                TN += 1
            elif last_term_is_leap_year and full_year:
                term_start_date += one_day

        pre_term = (term_start_date - pre_term_date).days
        pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        return pre_term, pre_remainder, TN, post_term, post_remainder

    def get_theoretical_time_fraction(self, payment_cycle=None, payment_date=None, outset_date=None, correct_leap_year=False):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        payment_date = payment_date if payment_date else self.maturity_date
        outset_date = outset_date if outset_date else self.outset_date

        pre_term, pre_remainder, TN, post_term, post_remainder = \
            self.parse_theoretical_terms(payment_cycle, payment_date, outset_date, False)

        time_fraction = (pre_remainder / pre_term) + TN + (post_remainder / post_term)

        return time_fraction

    def get_time_fraction(self, payment_cycle=None, payment_date=None, outset_date=None, correct_leap_year=False):
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        payment_date = payment_date if payment_date else self.maturity_date
        outset_date = outset_date if outset_date else self.outset_date
        f = 12 / payment_cycle

        pre_term, pre_remainder, TN, post_term, post_remainder = \
            self.parse_terms(payment_cycle, payment_date, outset_date, False)

        time_fraction = (pre_remainder / pre_term) + TN + (post_remainder / (365 / f))

        return time_fraction

    def get_price_conventional_maturity(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            for coupon_date in self.maturity_coupon_days[:-1]:
                price += self.get_dcv_conventional(self.untreated_coupon, discount_rate, self.payment_cycle, coupon_date)
            price += self.get_dcv_conventional(self.maturity_untreated_coupon, discount_rate)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate)
        elif self.type == 'compound':
            price += self.get_dcv_conventional(self.maturity_treated_coupon, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        elif self.type == 'compound-simple':
            price += self.get_dcv_conventional(self.maturity_treated_coupon, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        return price

    def get_sale_price_conventional(self, discount_rate):
        discount_rate = discount_rate if discount_rate else self.given_sale_discount_rate
        sale_date = self.maturity_sale_reference_date if self.maturity and self.given_sale_price else self.sale_date
        price = 0
        if self.type == 'coupon':
            cycle = self.payment_cycle
            maturity_coupon = self.maturity_untreated_coupon
            for coupon_date in self.unpaid_coupon_days[:-1]:
                price += self.get_dcv_sale(self.untreated_coupon, discount_rate, cycle, coupon_date, sale_date)
            price += self.get_dcv_sale(maturity_coupon, discount_rate, cycle, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, cycle, self.maturity_date, sale_date)
        elif self.type == 'compound':
            maturity_coupon = self.maturity_untreated_coupon if self.maturity else self.maturity_treated_coupon
            price = self.get_dcv_sale(maturity_coupon, discount_rate, 12, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, 12, self.maturity_date, sale_date)
        elif self.type == 'compound-simple':
            maturity_coupon = self.maturity_untreated_coupon if self.maturity else self.maturity_treated_coupon
            price = self.get_dcv_sale(maturity_coupon, discount_rate, 12, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, 12, self.maturity_date, sale_date)
        return price

    def get_price_conventional(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            for payment_date in self.payment_days:
                price += self.get_dcv_conventional(self.untreated_coupon, discount_rate, self.payment_cycle, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            sale_value = self.face_value * self.amount if self.sale_date_is_authentic else sale_price * self.amount
            price += self.get_dcv_conventional(sale_value, discount_rate, self.payment_cycle, self.sale_date)
        elif self.type == 'compound':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_conventional(sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_conventional(sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_price_conventional_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            first_income = self.untreated_coupon - self.first_tax if self.payment_number >= 1 else 0
            price += self.get_dcv_conventional(first_income, discount_rate, self.payment_cycle, self.coupon_days[0])
            for payment_date in self.payment_days[1:]:
                middle_income = self.untreated_coupon - self.middle_tax
                price += self.get_dcv_conventional(middle_income, discount_rate, self.payment_cycle, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            last_income = sale_price * self.amount - self.last_tax
            price += self.get_dcv_conventional(last_income, discount_rate, self.payment_cycle, self.sale_date)
        elif self.type == 'compound':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_conventional(net_sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_conventional(net_sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_price_theoretical(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            for payment_date in self.payment_days:
                price += self.get_dcv_theoretical(self.untreated_coupon, discount_rate, self.payment_cycle, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            sale_value = self.face_value * self.amount if self.sale_date_is_authentic else sale_price * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, self.payment_cycle, self.sale_date)
        elif self.type == 'compound':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_price_theoretical_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            first_income = self.untreated_coupon - self.first_tax if self.payment_number >= 1 else 0
            price += self.get_dcv_theoretical(first_income, discount_rate, self.payment_cycle, self.coupon_days[0])
            for payment_date in self.payment_days[1:]:
                middle_income = self.untreated_coupon - self.middle_tax
                price += self.get_dcv_theoretical(middle_income, discount_rate, self.payment_cycle, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            last_income = sale_price * self.amount - self.last_tax
            price += self.get_dcv_theoretical(last_income, discount_rate, self.payment_cycle, self.sale_date)
        elif self.type == 'compound':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_theoretical(net_sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_theoretical(net_sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_price_wook(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            for payment_date in self.payment_days:
                price += self.get_dcv_theoretical(self.untreated_coupon, discount_rate, 12, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            sale_value = self.face_value * self.amount if self.sale_date_is_authentic else sale_price * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            sale_value = int(self.sale_price) * self.amount
            price += self.get_dcv_theoretical(sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_price_wook_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            first_income = self.untreated_coupon - self.first_tax if self.payment_number >= 1 else 0
            price += self.get_dcv_theoretical(first_income, discount_rate, 12, self.coupon_days[0])
            for payment_date in self.payment_days[1:]:
                middle_income = self.untreated_coupon - self.middle_tax
                price += self.get_dcv_theoretical(middle_income, discount_rate, 12, payment_date)
            sale_price = self.sale_price if self.maturity else int(self.sale_price)
            last_income = sale_price * self.amount - self.last_tax
            price += self.get_dcv_theoretical(last_income, discount_rate, 12, self.sale_date)
        elif self.type == 'compound':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_theoretical(net_sale_value, discount_rate, 12, self.sale_date)
        elif self.type == 'compound-simple':
            net_sale_value = int(self.sale_price) * self.amount - self.last_tax
            price += self.get_dcv_theoretical(net_sale_value, discount_rate, 12, self.sale_date)
        return price

    def get_discount_rate_engine(self, get_price_func, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate_max = 200
        discount_rate = discount_rate_max / 2
        searching_gap = discount_rate_max / 2
        searching_number = 0
        while searching_number < 1000:
            searching_number += 1
            searching_gap /= 2
            dcv = get_price_func(discount_rate)
            rounded_dcv = round(dcv, 7)
            if rounded_dcv > purchase_value:
                discount_rate += searching_gap
            elif rounded_dcv < purchase_value:
                discount_rate -= searching_gap
            else:
                break
        return discount_rate

    def get_discount_rate_maturity(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional_maturity, purchase_value)
        return discount_rate

    def get_sale_discount_rate(self, sale_value):
        discount_rate = self.get_discount_rate_engine(self.get_sale_price_conventional, sale_value)
        return discount_rate

    def get_discount_rate(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional, purchase_value)
        return discount_rate

    def get_discount_rate_tax(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional_tax, purchase_value)
        return discount_rate

    def get_discount_rate_theoretical(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_theoretical, purchase_value)
        return discount_rate

    def get_discount_rate_theoretical_tax(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_theoretical_tax, purchase_value)
        return discount_rate

    def get_discount_rate_wook(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_wook, purchase_value)
        return discount_rate

    def get_discount_rate_wook_tax(self, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate = self.get_discount_rate_engine(self.get_price_wook_tax, purchase_value)
        return discount_rate

    def get_dcv(self, future_value, discount_rate, term_number, remainder_days, frequency=None, term=None, post_remainder=None):
        f = frequency if frequency else self.frequency
        r = discount_rate / 100
        d = remainder_days
        term = term if term else 365
        R = post_remainder if post_remainder is not None else (365 / f)
        term_number -= 1 if term_number or not post_remainder else 0

        dcv = future_value / \
              ((1 + (r / f) * (d / term)) * ((1 + r / f) ** term_number) * (1 + (r * (R / 365))))

        return dcv

    def calculate_dcv_theoretical(self, future_value, discount_rate=None, remaining_days=None, frequency=None, term=None):
        remaining_days = remaining_days if remaining_days is not None else self.remaining_days
        r = discount_rate if discount_rate is not None else self.given_discount_rate
        f = frequency if frequency else self.frequency
        term = 365 / f if not term else term
        r /= 100

        dcv = future_value / \
              ((1 + (r / f)) ** (remaining_days / term))

        return dcv

    def calculate_theoretical_price(self, coupon, maturity_value, discount_rate, total_remaining_days, frequency):
        coupon_period = 365 / frequency
        coupon_number = math.ceil(total_remaining_days / coupon_period)
        term_number = coupon_number - 1
        remainder_days = total_remaining_days - coupon_period * term_number

        price = 0
        remaining_days = 0
        for coupon_index in range(coupon_number):
            remaining_days = remainder_days + coupon_period * coupon_index
            price += self.calculate_dcv_theoretical(coupon, discount_rate, remaining_days, frequency)
        price += self.calculate_dcv_theoretical(maturity_value, discount_rate, remaining_days, frequency)
        return price

    def calculate_conventional_price(self, coupon, maturity_value, discount_rate, total_remaining_days, frequency):
        coupon_period = 365 / frequency
        coupon_number = math.ceil(total_remaining_days / coupon_period)
        term_number = coupon_number - 1
        remainder_days = total_remaining_days - coupon_period * term_number

        price = 0
        for coupon_index in range(coupon_number):
            price += self.get_dcv(coupon, discount_rate, coupon_index, remainder_days, frequency)
        price += self.get_dcv(maturity_value, discount_rate, term_number, remainder_days, frequency)
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
            price += self.calculate_dcv_theoretical(coupon, discount_rate, remaining_days, 1)
        # price += self.get_dcv_theoretical(maturity_value, discount_rate, remaining_days, frequency)
        price += self.calculate_dcv_theoretical(maturity_value, discount_rate, remaining_days, 1)
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

    def analyze(self):
        self.estimate_prices()
        self.estimate_profit()
        self.estimate_duration()
        self.report()

    def estimate_prices(self):
        if self.given_price:
            self.price_maturity = self.given_price
            self.price = self.given_price
            self.discount_rate_maturity = int(self.get_discount_rate_maturity() * 1000) / 1000
        elif self.given_discount_rate:
            self.price_maturity = int(self.get_price_conventional_maturity() / self.amount * 1000) / 1000
            self.discount_rate = self.given_discount_rate
            self.discount_rate_maturity = self.given_discount_rate
            self.price_is_given = False
        else:
            print('You should input one of information, price or discount rate')
            return

        if self.given_sale_price:
            self.sale_price = self.sale_assessment if self.maturity else self.given_sale_price
            self.sale_discount_rate = int(self.get_sale_discount_rate(self.given_sale_price * self.amount) * 1000) / 1000
        elif self.given_sale_discount_rate:
            self.sale_price = self.get_sale_price_conventional(self.given_sale_discount_rate) / self.amount
            self.sale_discount_rate = self.given_sale_discount_rate
        else:
            print('You should input one of information, sale price or sale discount rate')
            return

        if self.given_price:
            self.discount_rate = int(self.get_discount_rate() * 1000) / 1000
            self.discount_rate_tax = int(self.get_discount_rate_tax() * 1000) / 1000
            self.discount_rate_tax_bank = int(self.discount_rate_tax / 0.846 * 1000) / 1000
            self.discount_rate_theoretical = int(self.get_discount_rate_theoretical() * 1000) / 1000
            self.discount_rate_theoretical_tax = int(self.get_discount_rate_theoretical_tax() * 1000) / 1000
            self.discount_rate_theoretical_tax_bank = int(self.discount_rate_theoretical_tax / 0.846 * 1000) / 1000
            self.discount_rate_wook = int(self.get_discount_rate_wook() * 1000) / 1000
            self.discount_rate_wook_tax = int(self.get_discount_rate_wook_tax() * 1000) / 1000
            self.discount_rate_wook_tax_bank = int(self.discount_rate_wook_tax / 0.846 * 1000) / 1000
        elif self.given_discount_rate:
            self.price = int(self.get_price_conventional() / self.amount * 1000) / 1000
            self.price_tax = int(self.get_price_conventional_tax() / self.amount * 1000) / 1000
            self.price_theoretical = int(self.get_price_theoretical() / self.amount * 1000) / 1000
            self.price_theoretical_tax = int(self.get_price_theoretical_tax() / self.amount * 1000) / 1000
            self.price_wook = int(self.get_price_wook() / self.amount * 1000) / 1000
            self.price_wook_tax = int(self.get_price_wook_tax() / self.amount * 1000) / 1000
            self.price_is_given = False

    def estimate_profit(self):
        price = int(self.price_maturity)
        sale_price = self.sale_price if self.maturity else int(self.sale_price)
        self.capital_income_outset = int(self.outset_valuation * self.amount) - price * self.amount
        self.capital_income_sale = int(sale_price * self.amount - int(self.sale_assessment * self.amount))
        self.capital_income = self.capital_income_outset + self.capital_income_sale
        self.interest_income = self.valuation_profit + self.coupon_profit
        self.total_income = self.capital_income + self.interest_income

        self.capital_difference_outset = self.outset_valuation - self.price_maturity
        self.capital_difference_sale = self.sale_price - self.sale_assessment
        self.capital_income_actual = (self.capital_difference_outset + self.capital_difference_sale) * self.amount
        self.total_income_actual = self.capital_income_actual + self.interest_income
        self.capital_income_exhibit = int(self.total_income) - int(self.interest_income)

        self.profit_rate_annual_pretax = int(
            (self.total_income / (price * self.amount) * 100) / (self.remaining_days / 365) * 1000) / 1000
        self.profit = self.total_income - self.tax
        self.profit_rate = int(self.profit / (price * self.amount) * 100 * 100000) / 100000
        self.profit_rate_annual = int(
            (self.profit / (price * self.amount) * 100) / (self.remaining_days / 365) * 1000) / 1000
        self.profit_rate_bank = int(
            (self.profit / (price * self.amount) * 100) / (self.remaining_days / 365) / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(price * self.amount, price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

    def estimate_duration(self):
        discount_rate = self.discount_rate_maturity
        r1 = 0.01
        bp1 = 0.0001
        if self.type == 'coupon':
            r = discount_rate / self.frequency / 100
            weighted_dcv = 0
            total_dcv = 0
            convexity_denominator = 0
            for coupon_date in self.maturity_coupon_days[:-1]:
                time_fraction = self.get_time_fraction(self.payment_cycle, coupon_date)
                dcv = self.get_dcv_conventional(self.untreated_coupon, discount_rate, self.payment_cycle, coupon_date)
                total_dcv += dcv
                weighted_dcv += dcv * time_fraction
                convexity_denominator += dcv * time_fraction * (time_fraction + 1)
            time_fraction = self.get_time_fraction(self.payment_cycle, self.maturity_date)
            dcv = self.get_dcv_conventional(self.maturity_untreated_coupon + self.maturity_value, discount_rate)
            total_dcv += dcv
            weighted_dcv += dcv * time_fraction
            convexity_denominator += dcv * time_fraction * (time_fraction + 1)
            self.duration = int(weighted_dcv / total_dcv / self.frequency * 1000) / 1000
            self.modified_duration = int((self.duration / (1 + r)) * 1000) / 1000
            self.convexity = int((convexity_denominator / total_dcv) / ((1 + r) ** 2) / (self.frequency ** 2) * 1000) / 1000
        else:
            r = discount_rate / 100
            time_fraction = self.get_time_fraction(12, self.maturity_date)
            self.duration = int(time_fraction * 1000) / 1000
            self.modified_duration = int(self.duration / (1 + r) * 1000) / 1000
            self.convexity = int(time_fraction * (time_fraction + 1) / ((1 + r) ** 2) * 1000) / 1000
        self.dollar_duration = int(self.modified_duration * self.price_maturity * 1000) / 1000
        self.positive_delta_price = int((self.modified_duration * r1 + (1/2) * self.convexity * (r1**2)) * 100 * 1000) / 1000
        self.negative_delta_price = int((-self.modified_duration * r1 + (1/2) * self.convexity * (r1**2)) * 100 * 1000) / 1000
        self.dv01 = int((self.modified_duration * bp1 - (1/2) * self.convexity * (bp1**2)) * self.price_maturity * 1000) / 1000

    def report(self):
        print('=========================')
        print('      Bond Analysis      ')
        print('=========================')
        print('name:', self.name)
        print('type:', self.type, '({:,.3f} / {:,})'.format(round(self.untreated_coupon, 5), self.treated_coupon))
        print('issue date   :', self.issue_date.strftime('%Y-%m-%d'))
        print('maturity date:', self.maturity_date.strftime('%Y-%m-%d'))
        print('sale date    :', self.sale_date.strftime('%Y-%m-%d'))
        print('outset date  :', self.outset_date.strftime('%Y-%m-%d'))
        print('remaining days: {} ({} years, {} months, {} days) ({} years, {} days)'.
              format(self.remaining_days, self.remaining_delta.years, self.remaining_delta.months, self.remaining_delta.days,
                     self.remaining_delta.years, self.year_remainder))
        print('face value: {:,}'.format(self.face_value))
        print('coupon rate: {:,.3f}%'.format(self.coupon_rate))
        print('coupon number: {:,}'.format(self.coupon_number))
        if self.coupon_number > 1:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.
                  format(str(self.coupon_days[0])[:10], int(self.untreated_coupon), self.first_tax_base, self.first_tax))
        for coupon_date in self.coupon_days[1:-1]:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.
                  format(str(coupon_date)[:10], int(self.untreated_coupon), self.middle_tax_base, self.middle_tax))
        print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.
              format(str(self.coupon_days[-1])[:10], int(round(self.last_coupon, 6)), self.last_tax_base, self.last_tax))

        print('\033[031mvaluation at outset : {:,.3f} ({:,.3f}) [{:,.3f}]\033[0m'.
              format(self.outset_valuation, self.price_maturity, self.capital_difference_outset))
        print('\033[031mvaluation at sale   : {:,.3f} ({:,.3f}) [{:,.3f}]\033[0m'.
              format(self.sale_assessment, self.sale_price, self.capital_difference_sale))
        print('valuation profit : {:>7,} ({:,.2f})'.format(self.valuation_profit, self.valuation_profit_actual))
        print('coupon profit    : {:>7,} ({:,.2f})'.format(self.coupon_profit, self.coupon_profit_actual))
        print('interest income  : {:>7,} ({:,.2f})'.format(int(self.interest_income), self.interest_income))
        print('capital income   : {:>7,} ({:,.2f})'.format(self.capital_income_exhibit, self.capital_income_actual))
        print('total income     : {:>7,} ({:,.2f})'.format(int(self.total_income), self.total_income_actual))
        print('tax: {:,}'.format(self.tax))
        print('profit: {:,}'.format(int(self.profit)))
        print('profit rate: {:,.3f}%'.format(self.profit_rate))
        print('profit rate(CAGR): {:,.3f}%'.format(self.CAGR))
        print('profit rate(bank(C)): {:,.3f}%'.format(self.CAGR_bank))
        print('profit rate(pretax): {:,}%'.format(self.profit_rate_annual_pretax))
        print('\033[096mprofit rate(annual): {:,}%\033[0m'.format(self.profit_rate_annual))
        print('\033[096mprofit rate(bank(A)): {:,}%\033[0m'.format(self.profit_rate_bank))
        print('\033[094mprice(S): {:,.3f} ({:,})\033[0m'.format(self.sale_price, self.given_sale_price))
        print('\033[094mdiscount rate(S): {:,}%\033[0m'.format(self.sale_discount_rate))
        if self.price_is_given:
            print('\033[095mprice: {:,}\033[0m'.format(self.price))
            print('\033[095mdiscount rate(M): {}%\033[0m'.format(self.discount_rate_maturity))
            print('\033[091mdiscount rate(C): {}%\033[0m'.format(self.discount_rate))
            print('\033[091mdiscount rate(X): {}%\033[0m'.format(self.discount_rate_tax))
            print('\033[091mdiscount rate(B): {}%\033[0m'.format(self.discount_rate_tax_bank))
            print('\033[092mdiscount rate(T): {}%\033[0m'.format(self.discount_rate_theoretical))
            print('\033[092mdiscount rate(X): {}%\033[0m'.format(self.discount_rate_theoretical_tax))
            print('\033[092mdiscount rate(B): {}%\033[0m'.format(self.discount_rate_theoretical_tax_bank))
            print('\033[093mdiscount rate(W): {}%\033[0m'.format(self.discount_rate_wook))
            print('\033[093mdiscount rate(X): {}%\033[0m'.format(self.discount_rate_wook_tax))
            print('\033[093mdiscount rate(B): {}%\033[0m'.format(self.discount_rate_wook_tax_bank))
        else:
            print('\033[095mdiscount rate: {}%\033[0m'.format(self.discount_rate))
            print('\033[095mprice(M): {:,}\033[0m'.format(self.price_maturity))
            print('\033[091mprice(C): {:,}\033[0m'.format(self.price))
            print('\033[091mprice(X): {:,}\033[0m'.format(self.price_tax))
            print('\033[092mprice(T): {:,}\033[0m'.format(self.price_theoretical))
            print('\033[092mprice(X): {:,}\033[0m'.format(self.price_theoretical_tax))
            print('\033[093mprice(W): {:,}\033[0m'.format(self.price_wook))
            print('\033[093mprice(X): {:,}\033[0m'.format(self.price_wook_tax))
        print('============================')

        print('duration(O): {:,}'.format(self.duration))
        print('\033[096mduration(M): {:,}\033[0m'.format(self.modified_duration))
        # print('duration(D): {:,}'.format(self.dollar_duration))
        print('\033[096mconvexity: {:,}\033[0m'.format(self.convexity))
        print('PD price (1%): {:>6,}%'.format(self.positive_delta_price))
        print('ND price (1%): {:>6,}%'.format(self.negative_delta_price))
        print('DV01: {:,}'.format(self.dv01))

item = BondItem()
# item.set(c36)
# item.set(c50)
# item.set(c51)
# item.set(c52)
# item.set(c53)
# item.set(c54)
# item.set(c55)
# item.set(c56)
# item.set(c57)
# item.set(s09)
item.set(p05)
# item.set(p06)
# item.set(p33)
# item.set(p35)
# item.set(p36)
# item.set(p37)
# item.set(p38)
# item.set(p39)
bond = Bond(item)
bond.analyze()