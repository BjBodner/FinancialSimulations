import numpy as np
from utils import *


class Income:
    def __init__(self):
        self.age = 0

    def increment_by_one_year(self):
        self.age += 1

    def get_income(self): # in thousands of shekels, per month
        raise NotImplementedError


class Parent(Income):
    def __init__(self, 
        dict_of_monthly_incomes, # jobs go here
        dict_of_portfolios = {}
    ):
        self.dict_of_monthly_incomes = dict_of_monthly_incomes
        self.dict_of_portfolios = dict_of_portfolios

    def get_monthly_incomes(self):
        total_incomes = 0
        for monthly_income_name in self.dict_of_monthly_incomes.keys():
            income_dict = self.dict_of_monthly_incomes[monthly_income_name].get_income()
            self.update_job_related_portfolios(income_dict)
            total_incomes += income_dict[MONTHLY_INCOME_WITH_BONUSES]
        return total_incomes

    def update_job_related_portfolios(self, income_dict):
        for portfolio_name in JOB_RELATED_PORTFOLIOS:
            amount_to_deposite = income_dict[portfolio_name]
            self.dict_of_portfolios[portfolio_name].invest_in_portfolio(amount_to_deposite)

    def invest_in_main_portfolio(self, investment):
        self.dict_of_portfolios[NAME_OF_MAIN_PORTFOLION].invest_in_portfolio(investment)

    def withdraw_from_portfolio(self, portfolio_name, amount_to_withdraw):
        portfolio = self.dict_of_portfolios[portfolio_name]

        # extract the maximal amount possible from the portfolio
        if portfolio.balance_will_remain_above_minimal_amount_after_withdrawl(amount_to_withdraw):
            amount_withdrawn = portfolio.withdraw_from_portfolio(amount_to_withdraw)
            remaining_amount_to_withdraw = 0
        else:
            reduced_amount_to_withdraw = (portfolio.total_balance - portfolio.minimal_amount_for_withdrawl) * (1 - portfolio.tax_rate_for_selling_stock)
            if reduced_amount_to_withdraw > 0:
                amount_withdrawn = portfolio.withdraw_from_portfolio(reduced_amount_to_withdraw)
                remaining_amount_to_withdraw = (amount_to_withdraw - amount_withdrawn)
            else:
                amount_withdrawn = 0
                remaining_amount_to_withdraw = amount_to_withdraw

        return amount_withdrawn, remaining_amount_to_withdraw


    def withdraw_from_main_portfolio(self, amount_to_withdraw):
        remaining_amount_to_withdraw = amount_to_withdraw
        total_amount_withdrawn = 0
        for portfolio_name in [NAME_OF_MAIN_PORTFOLION, "keren_hishtalmut", "company_stock", "pension"]: # the order of portfolios to go through should be defined by the user
            if remaining_amount_to_withdraw > 0:
                amount_withdrawn, remaining_amount_to_withdraw = self.withdraw_from_portfolio(portfolio_name, remaining_amount_to_withdraw)
                total_amount_withdrawn += amount_withdrawn
            else:
                break

        return total_amount_withdrawn


    def increment_by_one_year(self):
        for income_name in self.dict_of_monthly_incomes.keys():
            self.dict_of_monthly_incomes[income_name].increment_by_one_year()

    def increment_by_one_month(self):
        for portfolio_name in self.dict_of_portfolios.keys():
            self.dict_of_portfolios[portfolio_name].increment_by_one_month()


class TotalIncomes:
    def __init__(self, dict_of_parents):
        self.dict_of_parents = dict_of_parents

    def remove_monthly_income(self, parent_name, monthly_income_name):
        del self.dict_of_parents[parent_name].dict_of_monthly_incomes[monthly_income_name]

    def increment_by_one_year(self):
        for parent_name in self.dict_of_parents.keys():
            self.dict_of_parents[parent_name].increment_by_one_year()

    def increment_by_one_month(self):
        for parent_name in self.dict_of_parents.keys():
            self.dict_of_parents[parent_name].increment_by_one_month()

    def get_monthly_incomes(self):
        # TODO output a dict of the incomes per parent
        total_income = 0
        for parent_name in self.dict_of_parents.keys():
            total_income += self.dict_of_parents[parent_name].get_monthly_incomes()
        return total_income

    def get_portfolios(self):
        portfolios = {}
        for parent_name in self.dict_of_parents.keys():
            portfolios[parent_name] = {portfolio_name: portfolio.total_balance for portfolio_name, portfolio in self.dict_of_parents[parent_name].dict_of_portfolios.items()}
        return portfolios

    def withdraw_from_main_portfolio(self, parent_name, amount_to_withdraw):
        return self.dict_of_parents[parent_name].withdraw_from_main_portfolio(amount_to_withdraw) 

    def invest_in_main_portfolio(self, parent_name, investment):
        return self.dict_of_parents[parent_name].invest_in_main_portfolio(investment)



class PortFolio:
    def __init__(self, amount_invested, annual_growth_percentage=5, minimal_amount_for_withdrawl=50, tax_rate_for_selling_stock=0.25):
        self.amount_invested = amount_invested
        self.total_balance = amount_invested
        self.tax_rate_for_selling_stock = tax_rate_for_selling_stock
        self.minimal_amount_for_withdrawl = minimal_amount_for_withdrawl

        # calc monthly growth factor
        annual_growth_factor = 1 + annual_growth_percentage/100
        self.monthly_growth_factor = annual_growth_factor**(1/12)

    def balance_will_remain_above_minimal_amount_after_withdrawl(self, amount_to_withdraw):
        amount_of_stocks_to_liquidate = amount_to_withdraw / (1 - self.tax_rate_for_selling_stock)
        expected_new_balance = (self.total_balance - amount_of_stocks_to_liquidate)
        return (expected_new_balance > self.minimal_amount_for_withdrawl)

    def invest_in_portfolio(self, investment):
        self.amount_invested += investment
        self.total_balance += investment

    def withdraw_from_portfolio(self, amount_to_withdraw):
        amount_of_stocks_to_liquidate = amount_to_withdraw / (1 - self.tax_rate_for_selling_stock)
        self.amount_invested -= amount_of_stocks_to_liquidate
        self.total_balance -= amount_of_stocks_to_liquidate
        if self.total_balance < (self.minimal_amount_for_withdrawl - 1):
            raise ValueError(f"portfolio exceeeded minimal amount")
        return amount_to_withdraw

    def increment_by_one_month(self):
        self.total_balance = self.total_balance * self.monthly_growth_factor



class Job(Income):
    def __init__(self, 
        base_salary_after_taxes, 
        probability_of_loosing_job=0.2, 
        percentage_of_base_salary_for_stocks=0.1, 
        bonus_fraction_of_annual_income=0.1, 
        options_per_year=30,
        has_pension_plan=True,
        has_keren_hishtalmut_plan=True,
        has_yearly_bonuses=True,
        phd=False, 
        mba=False, 
    ):
        super().__init__()
        self.base_salary_after_taxes = base_salary_after_taxes
        self.probability_of_loosing_job = probability_of_loosing_job
        self.percentage_of_base_salary_for_stocks = percentage_of_base_salary_for_stocks
        self.bonus_fraction_of_annual_income = bonus_fraction_of_annual_income
        self.options_per_year = options_per_year
        self.has_pension_plan = has_pension_plan
        self.has_keren_hishtalmut_plan = has_keren_hishtalmut_plan
        self.has_yearly_bonuses = has_yearly_bonuses
        self.currently_working = True
        self.got_bonus = False
        self.phd = phd
        self.mba = mba

    def increment_by_one_year(self):
        random_number = np.random.rand(1)
        if random_number < self.probability_of_loosing_job:
            self.currently_working = False
        else:
            super().increment_by_one_year()
            self.currently_working = True
            if self.has_yearly_bonuses:
                self.got_bonus = False

    def get_initial_base_salary(self):
        if self.age <= 2:
            return self.base_salary_after_taxes
        elif 2 < self.age <= 4:
            return self.base_salary_after_taxes + 1
        elif 4 < self.age <= 7:
            return self.base_salary_after_taxes + 2
        elif 7 < self.age <= 10:
            return self.base_salary_after_taxes + 4
        elif 10 < self.age <= 15:
            return self.base_salary_after_taxes + 6
        elif 15 < self.age <= 20:
            return self.base_salary_after_taxes + 7
        elif 20 < self.age:
            return self.base_salary_after_taxes + 2

    def get_base_salary(self):
        base_salary = self.get_initial_base_salary()
        if self.phd:
            base_salary += 3
        if self.mba:
            base_salary += 2

        if self.currently_working:
            return base_salary
        else:
            return 0

    def get_income(self):
        base_salary = self.get_base_salary()
        keren_hishtalmut = self.get_keren_hishtalmut() if self.has_keren_hishtalmut_plan else 0
        pension = self.get_pension() if self.has_pension_plan  else 0
        base_salary, company_stock = self.company_stocks(base_salary)
        bonus = self.get_bonus()
        base_salary_with_bonuses =  base_salary + bonus
        options = self.options()

        return {
            MONTHLY_INCOME_WITH_BONUSES: base_salary_with_bonuses, 
            "keren_hishtalmut": keren_hishtalmut,
            "pension": pension,
            "company_stock": company_stock,
            "options": options
            }


    def get_keren_hishtalmut(self, percentage_of_base=0.1, income_tax=0.6):
        base_salary = self.get_base_salary()
        keren_hishtalmut = percentage_of_base * (base_salary / income_tax)
        return keren_hishtalmut

    def get_pension(self, percentage_of_base=0.083, income_tax=0.6):
        base_salary = self.get_base_salary()
        pension = percentage_of_base * (base_salary / income_tax)
        return pension

    def company_stocks(self, base_salary, discount=0.1):
        amount_to_buy_company_stock = self.percentage_of_base_salary_for_stocks * base_salary
        company_stock =  amount_to_buy_company_stock / (1 - discount)
        return base_salary, company_stock

    def options(self):
        return self.options_per_year / 12

    def get_bonus(self):
        base_salary = self.get_base_salary()
        expected_bonus_amount = 12 * base_salary * self.bonus_fraction_of_annual_income
        if self.got_bonus:
            total_bonus = 0  
        else:
            total_bonus = expected_bonus_amount
            self.got_bonus = True
        return total_bonus


class GradSchoolJob(Job):
    def __init__(self,
        base_salary_after_taxes=8, 
        probability_of_loosing_job=0, 
        percentage_of_base_salary_for_stocks=0.0, 
        bonus_fraction_of_annual_income=0.0, 
        options_per_year=0,
        has_pension_plan=False,
        has_keren_hishtalmut_plan=False,
        phd=False, 
        mba=False, 
        name="benjy"
        ):

        super().__init__(
            base_salary_after_taxes, 
            probability_of_loosing_job, 
            percentage_of_base_salary_for_stocks, 
            bonus_fraction_of_annual_income, 
            options_per_year,
            has_pension_plan,
            has_keren_hishtalmut_plan,
            phd, 
            mba, 
            name
        )


class PassiveIncomeStream(Income):
    def __init__(self, amount_per_month):
        super.__init__()
        self.amount_per_month = amount_per_month

    def get_income(self):
        return {MONTHLY_INCOME_WITH_BONUSES: self.amount_per_month, 
            "keren_hishtalmut": 0,
            "pension": 0,
            "company_stock": 0,
            "options": 0
            }