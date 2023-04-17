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
        self.last_untreated_coupon = 0
        self.last_treated_coupon = 0
        self.maturity_untreated_coupon = 0
        self.maturity_treated_coupon = 0
        self.interest_outset = 0
        self.interest_sale = 0
        self.valuation_outset = 0
        self.valuation_sale = 0
        self.valuation_profit = 0
        self.coupon_profit = 0
        self.interest_income = 0
        self.capital_income = 0
        self.capital_income_exhibit = 0
        self.capital_income_actual = 0
        self.capital_income_outset = 0
        self.capital_income_sale = 0
        self.total_income = 0
        self.total_income_actual = 0
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
        self.price_maturity = 0
        self.price_wook = 0
        self.price_wook_tax = 0
        self.price_wook_tax_bank = 0
        self.discount_rate = 0.0
        self.discount_rate_maturity = 0.0
        self.discount_rate_tax = 0.0
        self.discount_rate_wook = 0.0
        self.discount_rate_wook_tax = 0.0
        self.sale_price = 0
        self.sale_discount_rate = 0.0

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
        self.remaining_days = self.get_remaining_days()
        self.remaining_delta = relativedelta(self.sale_date, self.outset_date)
        self.coupon_period = 365 / self.frequency
        self.term = relativedelta(months=item.payment_cycle)
        self.term_number = self.get_term_number(self.sale_date)
        self.maturity_term_number = self.get_term_number(self.maturity_date)
        self.unpaid_term_number = self.get_term_number(self.maturity_date, self.sale_date)
        self.coupon_number = self.get_coupon_number(self.term_number)
        self.maturity_coupon_number = self.get_coupon_number(self.maturity_term_number)
        self.coupon_days = self.get_coupon_days(self.term_number, self.sale_date)
        self.maturity_coupon_days = self.get_coupon_days(self.maturity_term_number, self.maturity_date)
        self.unpaid_coupon_days = self.get_coupon_days(self.unpaid_term_number, self.maturity_date, self.sale_date)
        self.previous_coupon_date = self.get_previous_coupon_date()
        self.before_last_coupon_date = self.get_before_last_coupon_date(self.sale_date)
        self.maturity_before_last_coupon_date = self.get_before_last_coupon_date(self.maturity_date)

        # self.interest_outset_start_date = self.get_interest_start_date(self.outset_date)
        # self.interest_sale_start_date = self.get_interest_start_date(self.sale_date)

        self.first_coupon_date = self.coupon_days[0]
        self.sale_date_is_authentic = self.check_authenticity(self.sale_date)
        self.maturity_date_is_authentic = self.check_authenticity(self.maturity_date)
        self.set_coupons()
        self.set_maturity_coupons()
        self.set_valuations()
        self.tax = self.get_tax()

        # self.interest_outset = self.get_interest(10000, self.interest_outset_start_date, self.outset_date)
        # self.interest_sale = self.get_interest(10000, self.interest_sale_start_date, self.sale_date)
        # self.valuation_outset = 10000 + self.interest_outset
        # self.valuation_sale = 10000 + self.interest_sale
        # self.valuation_profit = (self.valuation_sale - self.valuation_outset) * self.amount
        # self.coupon_profit = self.untreated_coupon * self.term_number if self.type == 'coupon' else 0

    def get_term_number(self, end_date, start_date=None):
        start_date = start_date if start_date else self.outset_date
        corrected_sale_date = end_date - relativedelta(days=1)
        if self.type == 'coupon':
            corrected_coupon_count = self.get_prepaid_count(corrected_sale_date)
            prepaid_count = self.get_prepaid_count(start_date)
            term_number = corrected_coupon_count - prepaid_count
        else:
            remaining_delta = relativedelta(corrected_sale_date, start_date)
            remaining_months = remaining_delta.years * 12 + remaining_delta.months
            term_number = remaining_months // self.payment_cycle
        return term_number

    def get_coupon_number(self, term_number):
        coupon_number = 0
        if self.type == 'coupon':
            coupon_number = term_number + 1
        elif self.type == 'compound':
            coupon_number = 1
        elif self.type == 'compound-simple':
            coupon_number = 1
        elif self.type == 'discount':
            coupon_number = 0
        return coupon_number

    def get_remaining_days(self):
        day_span_date = self.sale_date - self.outset_date
        day_span = day_span_date.days
        return day_span

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

    def get_previous_coupon_date(self):
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(self.outset_date)
            previous_coupon_date = self.issue_date + self.term * prepaid_count
        else:
            previous_coupon_date = self.issue_date
        return previous_coupon_date

    def get_before_last_coupon_date(self, end_date):
        delta = relativedelta(end_date, self.issue_date)
        delta_months = delta.years * 12 + delta.months
        coupon_count = math.ceil(delta_months / self.payment_cycle)
        before_last_coupon_date = self.issue_date + (coupon_count - 1) * self.term
        return before_last_coupon_date

    def get_interest_start_date(self, end_date):
        if self.type == 'coupon':
            prepaid_count = self.get_prepaid_count(end_date)
            interest_start_date = self.issue_date + prepaid_count * self.term
        else:
            interest_start_date = self.issue_date
        return interest_start_date

    def check_authenticity(self, end_date):
        delta = relativedelta(end_date, self.issue_date)
        months = delta.years * 12 + delta.months
        remainder = months % self.payment_cycle + delta.days
        authenticity = False if remainder else True
        return authenticity

    def get_coupon_days(self, term_number, end_date, start_date=None):
        start_date = start_date if start_date else self.outset_date
        coupon_days = list()
        prepaid_count = self.get_prepaid_count(start_date)
        term_number = term_number if self.type == 'coupon' else 0
        for coupon_index in range(term_number):
            coupon_day = self.issue_date + self.term * (prepaid_count + coupon_index + 1)
            coupon_days.append(coupon_day)
        coupon_days.append(end_date)
        return coupon_days

    def set_coupons(self):
        if self.type == 'coupon':
            annual_interest = self.face_value * (self.coupon_rate / 100)
            term_interest = annual_interest / self.frequency
            self.untreated_coupon = round(term_interest * self.amount, 6)
            self.treated_coupon = int(term_interest) * self.amount
            if self.sale_date_is_authentic:
                self.last_untreated_coupon = self.untreated_coupon
                self.last_treated_coupon = self.treated_coupon
            else:
                last_period = self.sale_date - self.before_last_coupon_date
                self.last_untreated_coupon = annual_interest * (last_period.days / 365) * self.amount
                self.last_treated_coupon = int(annual_interest * (last_period.days / 365)) * self.amount
                # next_last_coupon_date = self.get_before_last_coupon_date(self.sale_date + self.term)
                # last_term = next_last_coupon_date - self.before_last_coupon_date
                # self.last_untreated_coupon = term_interest * (last_period.days / last_term.days) * self.amount
                # self.last_treated_coupon = int(term_interest * (last_period.days / last_term.days)) * self.amount
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.sale_date)
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            self.last_untreated_coupon = self.untreated_coupon
            self.last_treated_coupon = self.treated_coupon
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            compound_interest = self.get_interest(10000, self.issue_date, min(transition_date, self.sale_date))
            simple_interest_number = self.get_simple_interest_number(transition_date, self.sale_date)
            simple_interest = 10000 * (self.coupon_rate / 100) * simple_interest_number
            self.untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount
            self.last_untreated_coupon = self.untreated_coupon
            self.last_treated_coupon = self.treated_coupon

    def set_coupons_deprecated2(self):
        if self.type == 'coupon':
            annual_interest = self.face_value * (self.coupon_rate / 100)
            term_interest = annual_interest / self.frequency
            self.untreated_coupon = round(term_interest * self.amount, 6)
            self.treated_coupon = int(term_interest) * self.amount
            if self.sale_date_is_authentic:
                self.last_untreated_coupon = self.untreated_coupon
                self.last_treated_coupon = self.treated_coupon
            else:
                last_period = self.sale_date - self.before_last_coupon_date
                next_last_coupon_date = self.get_before_last_coupon_date(self.sale_date + self.term)
                last_term = next_last_coupon_date - self.before_last_coupon_date
                self.last_untreated_coupon = term_interest * (last_period.days / last_term.days) * self.amount
                self.last_treated_coupon = int(term_interest * (last_period.days / last_term.days)) * self.amount
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.sale_date)
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            self.last_untreated_coupon = self.untreated_coupon
            self.last_treated_coupon = self.treated_coupon
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            if self.sale_date <= transition_date:
                compound_interest = self.get_interest(10000, self.issue_date, self.sale_date)
                simple_interest = 0
            else:
                compound_interest = self.get_interest(10000, self.issue_date, transition_date)
                simple_interest_number = self.get_simple_interest_number(transition_date, self.sale_date)
                simple_interest = 10000 * (self.coupon_rate / 100) * simple_interest_number
            self.untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount
            self.last_untreated_coupon = self.untreated_coupon
            self.last_treated_coupon = self.treated_coupon

    def set_coupons_deprecated(self):
        if self.type == 'coupon':
            annual_interest = self.face_value * (self.coupon_rate / 100)
            term_interest = annual_interest / self.frequency
            self.untreated_coupon = round(term_interest * self.amount, 6)
            self.treated_coupon = int(term_interest) * self.amount
            if self.sale_date_is_authentic:
                self.last_untreated_coupon = self.untreated_coupon
                self.last_treated_coupon = self.treated_coupon
            else:
                last_period = self.sale_date - self.before_last_coupon_date
                self.last_untreated_coupon = annual_interest * (last_period.days / 365) * self.amount
                self.last_treated_coupon = int(annual_interest * (last_period.days / 365)) * self.amount
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.sale_date)
            self.untreated_coupon = interest * self.amount
            self.treated_coupon = int(interest) * self.amount
            self.last_untreated_coupon = self.untreated_coupon
            self.last_treated_coupon = self.treated_coupon
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            if self.sale_date <= transition_date:
                compound_interest = self.get_interest(10000, self.issue_date, self.sale_date)
                simple_interest = 0
            else:
                compound_interest = self.get_interest(10000, self.issue_date, transition_date)
                simple_interest_days = (self.sale_date - transition_date).days
                simple_interest_period = (self.maturity_date - transition_date).days
                simple_interest = 10000 * (self.coupon_rate / 100) * (simple_interest_days / simple_interest_period)
            self.last_untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.last_treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount

    def set_maturity_coupons(self):
        if self.type == 'coupon':
            annual_interest = self.face_value * (self.coupon_rate / 100)
            if self.maturity_date_is_authentic:
                self.maturity_untreated_coupon = self.untreated_coupon
                self.maturity_treated_coupon = self.treated_coupon
            else:
                maturity_last_period = self.maturity_date - self.maturity_before_last_coupon_date
                self.maturity_untreated_coupon = annual_interest * (maturity_last_period.days / 365) * self.amount
                self.maturity_treated_coupon = int(annual_interest * (maturity_last_period.days / 365)) * self.amount
        elif self.type == 'compound':
            interest = self.get_interest(10000, self.issue_date, self.maturity_date)
            self.maturity_untreated_coupon = interest * self.amount
            self.maturity_treated_coupon = int(interest) * self.amount
            # coupon = self.treated_coupon #국민주택22-10, 신한투자증권
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            compound_interest = self.get_interest(10000, self.issue_date, transition_date)
            simple_interest = 10000 * (self.coupon_rate / 100) * self.simple_interest_number
            self.maturity_untreated_coupon = (compound_interest + simple_interest) * self.amount
            self.maturity_treated_coupon = (int(compound_interest) + int(simple_interest)) * self.amount

    # def get_interest_income(self):
    #     if self.type == 'coupon':
    #         last_coupon = self.last_untreated_coupon if self.sale_date_is_authentic else 0
    #         interest_income = self.untreated_coupon * (self.coupon_number - 1) + last_coupon
    #     else:
    #         interest_income = self.untreated_coupon
    #         # self.interest_income_proper_actual = self.untreated_coupon - self.reimbursed_coupon
    #         # self.interest_income_proper = int(self.untreated_coupon - int(self.reimbursed_coupon))
    #     return interest_income

    def set_valuations(self):
        # self.interest_outset = self.get_interest(10000, self.interest_outset_start_date, self.outset_date)
        # self.interest_sale = self.get_interest(10000, self.interest_sale_start_date, self.sale_date)
        # self.valuation_outset = 10000 + self.interest_outset
        # self.valuation_sale = 10000 + self.interest_sale
        # self.valuation_profit = (self.valuation_sale - self.valuation_outset) * self.amount
        # self.coupon_profit = self.untreated_coupon * self.term_number if self.type == 'coupon' else 0

        if self.type == 'coupon':
            annual_interest = 10000 * (self.coupon_rate / 100)
            outset_interest_start_count = self.get_prepaid_count(self.outset_date)
            sale_interest_start_count = self.get_prepaid_count(self.sale_date)
            outset_interest_start_date = self.issue_date + outset_interest_start_count * self.term
            sale_interest_start_date = self.issue_date + sale_interest_start_count * self.term
            outset_period = self.outset_date - outset_interest_start_date
            sale_period = self.sale_date - sale_interest_start_date
            self.interest_outset = annual_interest * (outset_period.days / 365)
            self.interest_sale = annual_interest * (sale_period.days / 365)
            self.coupon_profit = self.untreated_coupon * self.term_number if self.type == 'coupon' else 0
        elif self.type == 'compound':
            self.interest_outset = self.get_interest(10000, self.issue_date, self.outset_date)
            self.interest_sale = self.get_interest(10000, self.issue_date, self.sale_date)
        elif self.type == 'compound-simple':
            self.interest_outset = self.get_interest(10000, self.issue_date, self.outset_date)
            self.interest_sale = self.get_interest(10000, self.issue_date, self.sale_date)
        self.valuation_outset = 10000 + self.interest_outset
        self.valuation_sale = 10000 + self.interest_sale
        self.valuation_profit = (self.valuation_sale - self.valuation_outset) * self.amount

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
                self.middle_tax_base = self.untreated_coupon
                self.middle_tax = self.calculate_tax(self.untreated_coupon)
            last_period = self.sale_date - self.before_last_coupon_date
            deduction_days = (self.outset_date - self.before_last_coupon_date).days
            deduction_days = deduction_days if deduction_days > 0 else 0
            last_coupon_deduction = int(self.last_untreated_coupon * (deduction_days / last_period.days))
            last_tax_base = int(self.last_untreated_coupon - last_coupon_deduction)
            self.last_tax_base = last_tax_base
            self.last_tax = self.calculate_tax(last_tax_base)
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        elif self.type == 'compound':
            deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
            deduction = deduction_unit * self.amount
            tax_base = int(self.untreated_coupon - int(deduction))  #삼성증권, 키움증권
            # tax_base = int(self.untreated_coupon - deduction)  #신한투자증권
            self.last_tax_base = tax_base
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            compound_deduction_unit = self.get_interest(10000, self.issue_date, min(transition_date, self.sale_date))
            compound_deduction = compound_deduction_unit * self.amount  # 키움증권, 삼성증권
            # compound_deduction = int(compound_deduction_unit * self.amount)
            simple_interest_number = self.get_simple_interest_number(transition_date, self.outset_date)
            simple_deduction = 10000 * (self.coupon_rate / 100) * self.amount * simple_interest_number
            # simple_deduction = int(10000 * (self.coupon_rate / 100) * self.amount * simple_interest_number)
            deduction = compound_deduction + simple_deduction
            tax_base = self.untreated_coupon - deduction
            self.last_tax_base = int(tax_base)
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        return tax

    def get_tax_deprecated2(self):
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
                self.middle_tax_base = self.untreated_coupon
                self.middle_tax = self.calculate_tax(self.untreated_coupon)
            last_period = self.sale_date - self.before_last_coupon_date
            deduction_days = (self.outset_date - self.before_last_coupon_date).days
            deduction_days = deduction_days if deduction_days > 0 else 0
            last_coupon_deduction = int(self.last_untreated_coupon * (deduction_days / last_period.days))
            last_tax_base = int(self.last_untreated_coupon - last_coupon_deduction)
            self.last_tax_base = last_tax_base
            self.last_tax = self.calculate_tax(last_tax_base)
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        elif self.type == 'compound':
            deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
            deduction = int(deduction_unit * self.amount) #삼성증권, 키움증권
            # deduction = deduction_unit * self.amount #신한투자증권
            tax_base = int(self.untreated_coupon - deduction)
            self.last_tax_base = tax_base
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        elif self.type == 'compound-simple':
            transition_date = self.issue_date + relativedelta(years=self.compound_interest_number)
            if self.outset_date < transition_date:
                deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
                deduction = int(deduction_unit * self.amount)
            else:
                compound_deduction_unit = self.get_interest(10000, self.issue_date, transition_date)
                # compound_deduction = int(compound_deduction_unit * self.amount)
                compound_deduction = compound_deduction_unit * self.amount #키움증권, 삼성증권
                simple_interest_number = self.get_simple_interest_number(transition_date, self.outset_date)
                simple_deduction = 10000 * (self.coupon_rate / 100) * self.amount * simple_interest_number
                # simple_deduction = int(10000 * (self.coupon_rate / 100) * self.amount * simple_interest_number)
                deduction = compound_deduction + simple_deduction
            tax_base = self.untreated_coupon - deduction
            self.last_tax_base = int(tax_base)
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
        return tax

    def get_tax_deprecated(self):
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
                self.middle_tax_base = self.untreated_coupon
                self.middle_tax = self.calculate_tax(self.untreated_coupon)
            last_period = self.sale_date - self.before_last_coupon_date
            deduction_days = (self.outset_date - self.before_last_coupon_date).days
            deduction_days = deduction_days if deduction_days > 0 else 0
            last_coupon_deduction = int(self.last_untreated_coupon * (deduction_days / last_period.days))
            last_tax_base = int(self.last_untreated_coupon - last_coupon_deduction)
            self.last_tax_base = last_tax_base
            self.last_tax = self.calculate_tax(last_tax_base)
            tax = self.first_tax + self.middle_tax * (self.coupon_number - 2) + self.last_tax
        elif self.type == 'compound':
            deduction_unit = self.get_interest(10000, self.issue_date, self.outset_date)
            deduction = int(deduction_unit * self.amount) #삼성증권, 키움증권
            # deduction = deduction_unit * self.amount #신한투자증권
            tax_base = int(self.untreated_coupon - deduction)
            self.last_tax_base = tax_base
            self.last_tax = self.calculate_tax(tax_base)
            tax = self.last_tax
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
            tax_base = int(self.untreated_coupon - deduction)
            self.last_tax_base = tax_base
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

    def get_years(self, start_date, end_date):
        delta = relativedelta(end_date, start_date)
        quotient_years = delta.years
        last_year = start_date + relativedelta(years=quotient_years)
        next_year = last_year + relativedelta(years=1)
        remaining_days = (end_date - last_year).days
        remaining_term = (next_year - last_year).days

        remaining_term = 365

        remaining_years = remaining_days / remaining_term
        years = quotient_years + remaining_years
        return years

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

    def get_term_days_deprecated(self, start_date, end_date, payment_cycle):
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        term_number = months // payment_cycle
        term_end_date = start_date + term_number * relativedelta(months=payment_cycle)
        remainder_days = (end_date - term_end_date).days
        return term_number, remainder_days

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

    def get_term_deprecated(self, start_date, term_number, payment_cycle=None):
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

    def parse_terms(self, payment_cycle=None, payment_date=None, outset_date=None, correct_leap_year=True):
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

    def get_dcv_conventional_deprecated0327(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle
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

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r * (post_remainder / 365))))

        return dcv

    def get_dcv_sale_deprecated(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle
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
        pre_term_is_leap_year = True if (term_start_date - pre_term_date).days == 366 else False
        pre_term_is_last_year = True if (term_end_date - term_start_date).days == 0 else False
        full_leap_year = True if (term_start_date - outset_date).days == 366 else False
        last_term_is_leap_year = True if (term_end_date - term_start_date).days == 366 else False
        full_year = True if (post_term_date - term_end_date).days == 0 else False
        sale_dcv = True
        if pre_term_is_leap_year and pre_term_is_last_year and not full_leap_year and not sale_dcv:
            pre_term_date = pre_term_date + one_day
        elif pre_term_is_leap_year and pre_term_is_last_year and full_leap_year and not sale_dcv:
            pre_term_date = pre_term_date - term_delta
            term_start_date = term_start_date - term_delta + one_day
            TN += 1
        elif last_term_is_leap_year and full_year and not sale_dcv:
            term_start_date += one_day

        pre_term = (term_start_date - pre_term_date).days
        pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r * (post_remainder / 365))))

        return dcv

    def get_dcv_conventional_deprecated(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle

        issue_outset_cycles = self.get_raw_prepaid_count(outset_date, payment_cycle)
        pre_term_start_count = int(issue_outset_cycles)
        term_start_count = pre_term_start_count + 1
        issue_payment_cycles = self.get_raw_prepaid_count(payment_date, payment_cycle)
        post_term_end_count = math.ceil(issue_payment_cycles)
        term_end_count = int(issue_payment_cycles)

        term_number = term_end_count - term_start_count
        TN = term_number if term_number > 0 else 0
        term_delta = relativedelta(months=payment_cycle)
        previous_term_date = self.issue_date + pre_term_start_count * term_delta
        term_start_date = self.issue_date + term_start_count * term_delta
        term_end_date = self.issue_date + term_end_count * term_delta
        post_term_date = self.issue_date + post_term_end_count * term_delta
        last_term = False if term_start_date <= term_end_date else True

        pre_term = (term_start_date - previous_term_date).days
        pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r * (post_remainder / 365))))

        return dcv

    def get_dcv_conventional_complete_term(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle

        issue_outset_cycles = self.get_raw_prepaid_count(outset_date, payment_cycle)
        pre_term_start_count = int(issue_outset_cycles)
        term_start_count = pre_term_start_count + 1
        issue_payment_cycles = self.get_raw_prepaid_count(payment_date, payment_cycle)
        post_term_end_count = math.ceil(issue_payment_cycles)
        term_end_count = post_term_end_count - 1

        term_number = term_end_count - term_start_count
        TN = term_number if term_number > 0 else 0
        term_delta = relativedelta(months=payment_cycle)
        previous_term_date = self.issue_date + pre_term_start_count * term_delta
        term_start_date = self.issue_date + term_start_count * term_delta
        term_end_date = self.issue_date + term_end_count * term_delta
        post_term_date = self.issue_date + post_term_end_count * term_delta

        last_term = False if term_start_date <= term_end_date else True
        sale_date_is_authentic_date = True if issue_payment_cycles - int(issue_payment_cycles) == 0 else False
        remaining_more_than_one_term = True if issue_payment_cycles - issue_outset_cycles >= 1 else False
        complete_term = True if sale_date_is_authentic_date and remaining_more_than_one_term else False

        pre_term = (term_start_date - previous_term_date).days
        # pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        pre_remainder = (term_start_date - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days if complete_term else 365 / f
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        dcv = future_value / \
              ((1 + (r / f) * (pre_remainder / pre_term)) * ((1 + r / f) ** TN) * (1 + (r / f) * (post_remainder / post_term)))

        return dcv

    def get_dcv_theoretical(self, future_value, discount_rate=None, payment_cycle=None, payment_date=None, outset_date=None):
        outset_date = outset_date if outset_date else self.outset_date
        payment_date = payment_date if payment_date else self.maturity_date
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle
        r = discount_rate / 100 if discount_rate else self.given_discount_rate / 100
        f = 12 / payment_cycle

        issue_outset_cycles = self.get_raw_prepaid_count(outset_date, payment_cycle)
        pre_term_start_count = int(issue_outset_cycles)
        term_start_count = pre_term_start_count + 1
        issue_payment_cycles = self.get_raw_prepaid_count(payment_date, payment_cycle)
        post_term_end_count = math.ceil(issue_payment_cycles)
        term_end_count = post_term_end_count - 1

        term_number = term_end_count - term_start_count
        TN = term_number if term_number > 0 else 0
        term_delta = relativedelta(months=payment_cycle)
        previous_term_date = self.issue_date + pre_term_start_count * term_delta
        term_start_date = self.issue_date + term_start_count * term_delta
        term_end_date = self.issue_date + term_end_count * term_delta
        post_term_date = self.issue_date + post_term_end_count * term_delta
        last_term = False if term_start_date <= term_end_date else True

        pre_term = (term_start_date - previous_term_date).days
        pre_remainder = (min(term_start_date, payment_date) - outset_date).days if not last_term else 0
        post_term = (post_term_date - term_end_date).days
        post_remainder = (payment_date - max(term_end_date, outset_date)).days

        dcv = future_value / \
              ((1 + (r / f)) ** ((pre_remainder / pre_term) + TN + (post_remainder / post_term)))

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
            price += self.get_dcv_theoretical(self.untreated_coupon, discount_rate, self.payment_cycle, coupon_date)
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate)
        return price

    def get_price_conventional(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            for coupon_date in self.coupon_days[:-1]:
                price += self.get_dcv_conventional(self.untreated_coupon, discount_rate, self.payment_cycle, coupon_date)
            price += self.get_dcv_conventional(self.last_untreated_coupon, discount_rate)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate)
        elif self.type == 'compound':
            price += self.get_dcv_conventional(self.treated_coupon, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        elif self.type == 'compound-simple':
            price += self.get_dcv_conventional(self.treated_coupon, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        return price

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
        maturity = True if self.sale_date == self.maturity_date else False
        sale_date = self.maturity_before_last_coupon_date if maturity and self.given_sale_price else self.sale_date
        maturity_coupon = self.maturity_untreated_coupon if maturity else self.maturity_treated_coupon
        price = 0
        if self.type == 'coupon':
            cycle = self.payment_cycle
            for coupon_date in self.unpaid_coupon_days[:-1]:
                price += self.get_dcv_sale(self.untreated_coupon, discount_rate, cycle, coupon_date, sale_date)
            # price += self.get_dcv_sale(self.maturity_treated_coupon, discount_rate, cycle, self.maturity_date, sale_date)
            price += self.get_dcv_sale(maturity_coupon, discount_rate, cycle, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, cycle, self.maturity_date, sale_date)
            # maturity_coupon = self.maturity_untreated_coupon
            # cycle = self.payment_cycle
            # for coupon_date in self.unpaid_coupon_days[:-1]:
            #     price += self.get_dcv_conventional(self.untreated_coupon, discount_rate, cycle, coupon_date, sale_date)
            # price += self.get_dcv_conventional(maturity_coupon, discount_rate, cycle, self.maturity_date, sale_date)
            # price += self.get_dcv_conventional(self.maturity_value, discount_rate, cycle, self.maturity_date, sale_date)
        elif self.type == 'compound':
            price = self.get_dcv_sale(maturity_coupon, discount_rate, 12, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, 12, self.maturity_date, sale_date)
        elif self.type == 'compound-simple':
            price = self.get_dcv_sale(maturity_coupon, discount_rate, 12, self.maturity_date, sale_date)
            price += self.get_dcv_sale(self.maturity_value, discount_rate, 12, self.maturity_date, sale_date)
        return price

    def get_price_conventional_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            first_income = self.untreated_coupon - self.first_tax if self.coupon_number > 1 else 0
            price += self.get_dcv_conventional(first_income, discount_rate, self.payment_cycle, self.coupon_days[0])
            for coupon_date in self.coupon_days[1:-1]:
                middle_income = self.untreated_coupon - self.middle_tax
                price += self.get_dcv_conventional(middle_income, discount_rate, self.payment_cycle, coupon_date)
            last_income = self.last_untreated_coupon - self.last_tax
            price += self.get_dcv_conventional(last_income, discount_rate)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate)
        elif self.type == 'compound':
            coupon_income = self.treated_coupon - self.last_tax
            price += self.get_dcv_conventional(coupon_income, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        elif self.type == 'compound-simple':
            coupon_income = self.treated_coupon - self.last_tax
            price += self.get_dcv_conventional(coupon_income, discount_rate, 12)
            price += self.get_dcv_conventional(self.maturity_value, discount_rate, 12)
        return price

    def get_price_wook(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        for coupon_date in self.coupon_days[:-1]:
            price += self.get_dcv_theoretical(self.untreated_coupon, discount_rate, 12, coupon_date)
        price += self.get_dcv_theoretical(self.last_untreated_coupon, discount_rate, 12)
        price += self.get_dcv_theoretical(self.maturity_value, discount_rate, 12)
        return price

    def get_price_wook_tax(self, discount_rate=None):
        discount_rate = discount_rate if discount_rate else self.given_discount_rate
        price = 0
        if self.type == 'coupon':
            first_income = self.untreated_coupon - self.first_tax if self.coupon_number > 1 else 0
            price += self.get_dcv_theoretical(first_income, discount_rate, 12, self.coupon_days[0])
            for coupon_date in self.coupon_days[1:-1]:
                middle_income = self.untreated_coupon - self.middle_tax
                price += self.get_dcv_theoretical(middle_income, discount_rate, 12, coupon_date)
            last_income = self.last_untreated_coupon - self.last_tax
            price += self.get_dcv_theoretical(last_income, discount_rate, 12)
            price += self.get_dcv_theoretical(self.maturity_value, discount_rate, 12)
        elif self.type == 'compound':
            price += self.get_dcv_theoretical(self.treated_coupon, discount_rate, 12)
            price += self.get_dcv_theoretical(self.maturity_value, discount_rate, 12)
        elif self.type == 'compound-simple':
            price += self.get_dcv_theoretical(self.treated_coupon, discount_rate, 12)
            price += self.get_dcv_theoretical(self.maturity_value, discount_rate, 12)
        return price

    def get_discount_rate_engine(self, get_price_func, purchase_value=None):
        purchase_value = purchase_value if purchase_value else self.purchase_value
        discount_rate_max = 100
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

    def get_discount_rate(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional, purchase_value)
        return discount_rate

    def get_discount_rate_maturity(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional_maturity, purchase_value)
        return discount_rate

    def get_sale_discount_rate(self, sale_value):
        discount_rate = self.get_discount_rate_engine(self.get_sale_price_conventional, sale_value)
        return discount_rate

    def get_discount_rate_tax(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_conventional_tax, purchase_value)
        return discount_rate

    def get_discount_rate_theoretical(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_theoretical, purchase_value)
        return discount_rate

    def get_discount_rate_wook(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_wook, purchase_value)
        return discount_rate

    def get_discount_rate_wook_tax(self, purchase_value=None):
        discount_rate = self.get_discount_rate_engine(self.get_price_wook_tax, purchase_value)
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
        price_is_given = True
        if self.given_price and not self.given_discount_rate:
            self.price = self.given_price
            self.discount_rate_maturity = int(self.get_discount_rate_maturity() * 1000) / 1000
            self.discount_rate = int(self.get_discount_rate() * 1000) / 1000
            self.discount_rate_tax = int(self.get_discount_rate_tax() * 1000) / 1000
            self.discount_rate_tax_bank = round(self.discount_rate_tax / 0.846, 3)
            self.discount_rate_wook = int(self.get_discount_rate_wook() * 1000) / 1000
            self.discount_rate_wook_tax = int(self.get_discount_rate_wook_tax() * 1000) / 1000
            self.discount_rate_wook_tax_bank = round(self.discount_rate_wook_tax / 0.846, 3)
        elif self.given_discount_rate:
            self.discount_rate = self.given_discount_rate
            self.price_maturity = round(self.get_price_conventional_maturity() / self.amount, 3)
            self.price = round(self.get_price_conventional() / self.amount, 3)
            self.price_wook = round(self.get_price_wook() / self.amount, 3)
            self.price_wook_tax = round(self.get_price_wook_tax() / self.amount, 3)
            price_is_given = False
        else:
            print('You should input one of information, price or discount rate')
            return

        if self.given_sale_price and not self.given_sale_discount_rate:
            self.sale_price = self.given_sale_price
            self.sale_discount_rate = int(self.get_sale_discount_rate(self.sale_price * self.amount) * 1000) / 1000
        elif self.given_sale_discount_rate:
            self.sale_discount_rate = self.given_sale_discount_rate
            # self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)
            self.sale_price = self.get_sale_price_conventional(self.sale_discount_rate) / self.amount
        else:
            # self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)
            self.sale_price = self.get_sale_price_conventional(self.sale_discount_rate) / self.amount

        price = int(self.price_maturity)
        sale_price = int(self.sale_price) if self.sale_date != self.maturity_date else self.sale_price
        self.capital_income_outset = (self.valuation_outset - price) * self.amount
        self.capital_income_sale = (sale_price - self.valuation_sale) * self.amount
        capital_income_outset_actual = (self.valuation_outset - self.price_maturity) * self.amount
        capital_income_sale_actual = (self.sale_price - self.valuation_sale) * self.amount
        self.capital_income_actual = capital_income_outset_actual + capital_income_sale_actual
        self.capital_income = self.capital_income_outset + self.capital_income_sale
        self.interest_income = (self.valuation_sale - self.valuation_outset) * self.amount + self.coupon_profit
        self.total_income_actual = self.capital_income_actual + self.interest_income
        self.total_income = self.capital_income + self.interest_income
        self.capital_income_exhibit = int(self.total_income) - int(self.interest_income)

        self.profit = self.total_income - self.tax
        self.profit_rate = int(self.profit / (price * self.amount) * 100 * 1000000) / 1000000
        self.profit_rate_annual = int(self.profit_rate / (self.remaining_days / 365) * 1000) / 1000
        self.profit_rate_bank = int(self.profit_rate / (self.remaining_days / 365) / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(price * self.amount, price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

        self.report(price_is_given)

    def analyze_deprecated2(self):
        price_is_given = True
        if self.given_price and not self.given_discount_rate:
            self.price = self.given_price
            self.discount_rate_maturity = int(self.get_discount_rate_maturity() * 1000) / 1000
            self.discount_rate = int(self.get_discount_rate() * 1000) / 1000
            self.discount_rate_tax = int(self.get_discount_rate_tax() * 1000) / 1000
            self.discount_rate_tax_bank = round(self.discount_rate_tax / 0.846, 3)
            self.discount_rate_wook = int(self.get_discount_rate_wook() * 1000) / 1000
            self.discount_rate_wook_tax = int(self.get_discount_rate_wook_tax() * 1000) / 1000
            self.discount_rate_wook_tax_bank = round(self.discount_rate_wook_tax / 0.846, 3)
        elif self.given_discount_rate:
            self.discount_rate = self.given_discount_rate
            self.price_maturity = round(self.get_price_conventional_maturity() / self.amount, 3)
            self.price = round(self.get_price_conventional() / self.amount, 3)
            self.price_wook = round(self.get_price_wook() / self.amount, 3)
            self.price_wook_tax = round(self.get_price_wook_tax() / self.amount, 3)
            price_is_given = False
        else:
            print('You should input one of information, price or discount rate')
            return

        if self.given_sale_price and not self.given_sale_discount_rate:
            self.sale_price = self.given_sale_price
            self.sale_discount_rate = int(self.get_sale_discount_rate(self.sale_price * self.amount) * 1000) / 1000
        elif self.given_sale_discount_rate:
            self.sale_discount_rate = self.given_sale_discount_rate
            self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)
        else:
            self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)

        sale_price = int(self.sale_price) if self.sale_date != self.maturity_date else self.sale_price
        self.total_income = (sale_price - int(self.price_maturity)) * self.amount
        self.capital_income = int(self.total_income) - int(self.interest_income_proper)
        self.total_income_actual = (self.sale_price - self.price_maturity) * self.amount
        self.capital_income_actual = self.total_income_actual - self.interest_income_proper_actual

        price = int(self.price_maturity)
        self.profit = self.total_income - self.tax
        self.profit_rate = int(self.profit / (price * self.amount) * 100 * 1000000) / 1000000
        self.profit_rate_annual = int(self.profit_rate / (self.remaining_days / 365) * 1000) / 1000
        self.profit_rate_bank = int(self.profit_rate / (self.remaining_days / 365) / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(price * self.amount, price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

        self.report(price_is_given)

    def analyze_deprecated(self):
        price_is_given = True
        if self.given_price and not self.given_discount_rate:
            self.price = self.given_price
            self.discount_rate_maturity = int(self.get_discount_rate_maturity() * 1000) / 1000
            self.discount_rate = int(self.get_discount_rate() * 1000) / 1000
            self.discount_rate_tax = int(self.get_discount_rate_tax() * 1000) / 1000
            self.discount_rate_tax_bank = round(self.discount_rate_tax / 0.846, 3)
            self.discount_rate_wook = int(self.get_discount_rate_wook() * 1000) / 1000
            self.discount_rate_wook_tax = int(self.get_discount_rate_wook_tax() * 1000) / 1000
            self.discount_rate_wook_tax_bank = round(self.discount_rate_wook_tax / 0.846, 3)
        elif self.given_discount_rate:
            self.discount_rate = self.given_discount_rate
            self.price_maturity = round(self.get_price_conventional_maturity() / self.amount, 3)
            self.price = round(self.get_price_conventional() / self.amount, 3)
            self.price_wook = round(self.get_price_wook() / self.amount, 3)
            self.price_wook_tax = round(self.get_price_wook_tax() / self.amount, 3)
            price_is_given = False
        else:
            print('You should input one of information, price or discount rate')
            return

        if self.given_sale_price and not self.given_sale_discount_rate:
            self.sale_price = self.given_sale_price
            self.sale_discount_rate = int(self.get_sale_discount_rate(self.sale_price * self.amount) * 1000) / 1000
        elif self.given_sale_discount_rate:
            self.sale_discount_rate = self.given_sale_discount_rate
            self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)
        else:
            self.sale_price = round(self.get_sale_price_conventional(self.sale_discount_rate) / self.amount, 3)

        price = int(self.price)
        self.capital_income = int(self.maturity_value - price * self.amount)
        arbitrage = (self.sale_price - self.price) * self.amount
        # self.capital_income = arbitrage - self.interest_income
        self.total_income = self.interest_income + self.capital_income
        self.profit = self.total_income - self.tax
        self.profit_rate = int(self.profit / (price * self.amount) * 100 * 1000000) / 1000000
        self.profit_rate_annual = int(self.profit_rate / (self.remaining_days / 365) * 1000) / 1000
        self.profit_rate_bank = int(self.profit_rate / (self.remaining_days / 365) / 0.846 * 1000) / 1000
        self.CAGR = self.get_CAGR(price * self.amount, price * self.amount + self.profit, self.remaining_days) * 100
        self.CAGR_bank = self.CAGR / 0.846

        self.report(price_is_given)

    def report(self, price_is_given):
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
                     self.remaining_delta.years, self.remaining_days - self.remaining_delta.years * 365))
        print('face value: {:,}'.format(self.face_value))
        print('coupon rate: {:,.3f}%'.format(self.coupon_rate))
        print('coupon number: {:,}'.format(self.coupon_number))
        if self.coupon_number > 1:
            print('\033[032mcoupon {} ({:,}) - [{:,.1f}] {:,}\033[0m'.
                  format(str(self.coupon_days[0])[:10], self.untreated_coupon, self.first_tax_base, self.first_tax))
        for coupon_date in self.coupon_days[1:-1]:
            print('\033[032mcoupon {} ({:,}) - [{:,}] {:,}\033[0m'.
                  format(str(coupon_date)[:10], self.untreated_coupon, self.middle_tax_base, self.middle_tax))
        print('\033[032mcoupon {} ({:,.1f}) - [{:,.1f}] {:,}\033[0m'.
              format(str(self.coupon_days[-1])[:10], self.last_untreated_coupon, self.last_tax_base, self.last_tax))
        print('\033[031mvaluation at outset : {:,.3f} ({:,.3f}) [{:,.3f}]\033[0m'.
              format(self.valuation_outset, self.price_maturity, self.capital_income_outset))
        print('\033[031mvaluation at sale   : {:,.3f} ({:,.3f}) [{:,.3f}]\033[0m'.
              format(self.valuation_sale, self.sale_price, self.capital_income_sale))
        print('valuation profit : {:,.2f}'.format(self.valuation_profit))
        print('coupon profit    : {:,.2f}'.format(self.coupon_profit))
        print('interest income  : {:,} ({:,.2f})'.format(int(self.interest_income), self.interest_income))
        print('capital income   : {:,} ({:,.2f})'.format(self.capital_income_exhibit, self.capital_income_actual))
        print('total income     : {:,} ({:,.2f})'.format(int(self.total_income), self.total_income_actual))
        print('tax: {:,}'.format(self.tax))
        print('profit: {:,}'.format(int(self.profit)))
        print('profit rate: {:,.3f}%'.format(self.profit_rate))
        print('profit rate(CAGR): {:,.3f}%'.format(self.CAGR))
        print('profit rate(bank(C)): {:,.3f}%'.format(self.CAGR_bank))
        print('\033[096mprofit rate(annual): {:,.3f}%\033[0m'.format(self.profit_rate_annual))
        print('\033[096mprofit rate(bank(A)): {:,.3f}%\033[0m'.format(self.profit_rate_bank))
        print('\033[094mprice(S): {:,.3f}\033[0m'.format(self.sale_price))
        print('\033[094mdiscount rate(S): {:,}%\033[0m'.format(self.sale_discount_rate))
        if price_is_given:
            print('\033[095mprice: {:,}\033[0m'.format(self.price))
            print('\033[095mdiscount rate(M): {}%\033[0m'.format(self.discount_rate_maturity))
            print('\033[091mdiscount rate(C): {}%\033[0m'.format(self.discount_rate))
            print('\033[091mdiscount rate(T): {}%\033[0m'.format(self.discount_rate_tax))
            print('\033[091mdiscount rate(B): {}%\033[0m'.format(self.discount_rate_tax_bank))
            print('\033[093mdiscount rate(W): {}%\033[0m'.format(self.discount_rate_wook))
            print('\033[093mdiscount rate(T): {}%\033[0m'.format(self.discount_rate_wook_tax))
            print('\033[093mdiscount rate(B): {}%\033[0m'.format(self.discount_rate_wook_tax_bank))
        else:
            print('\033[095mdiscount rate: {}%\033[0m'.format(self.discount_rate))
            print('\033[095mprice(M): {:,}\033[0m'.format(self.price_maturity))
            print('\033[095mprice(C): {:,}\033[0m'.format(self.price))
            print('\033[093mprice(W): {:,}\033[0m'.format(self.price_wook))
            print('\033[093mprice(T): {:,}\033[0m'.format(self.price_wook_tax))
        print('============================')


item = BondItem()
item.set(c36)
bond = Bond(item)
bond.analyze()