import numpy as np
import matplotlib.pyplot as plt
import yaml

from expenses import (
    TotalExpenses,
    MBA,
    BigFamilyTrip,
    SmallFamilyTrip,
    WeekendTrips,
    Bills,
    Kid,
    Pet,
    Fun,
    LivingExpenses,
    House,
    FixedPriceApartment,
    LocationDependentApartment,
    Car
)
from incomes import (
    PortFolio,
    PassiveIncomeStream,
    Job,
    Parent,
    TotalIncomes
)
from utils import NAME_OF_MAIN_PORTFOLION, JOB_RELATED_PORTFOLIOS, NAMES_OF_PARENTS, PortFolioTracker




class FinancialSimulator:

    def __init__(self, config_path):
        self.config = self.load_config(config_path)

        self.total_incomes = self.get_initial_incomes()
        self.total_expenses = self.get_initial_expenses()
        self.balance_in_bank_account = 0 # TODO load this from the config
        self.total_num_months = 0 # TODO load this from the config
        self.num_years = 35 # TODO load this from the config
        self.portfolio_tracker = None


    def load_config(self, config_path):
        with open(config_path, "r") as fh:
            return yaml.load(fh, yaml.FullLoader)

    def get_initial_incomes(self):

        # create benjy
        benjy_job = Job(
                base_salary_after_taxes=18.5, 
                probability_of_loosing_job=0.2, 
                percentage_of_base_salary_for_stocks=0.0, 
                bonus_fraction_of_annual_income=0.0, 
                dollar_amount_per_year=0,
                has_pension_plan=True,
                has_keren_hishtalmut_plan=True,
            )
        benjy_dict_of_portfolios = {NAME_OF_MAIN_PORTFOLION: PortFolio(amount_invested=100, minimal_amount_for_withdrawl=50)}
        for portfolio_name in JOB_RELATED_PORTFOLIOS:
            benjy_dict_of_portfolios[portfolio_name] = PortFolio(
                amount_invested=0, 
                tax_rate_for_selling_stock=0 if portfolio_name == "keren_hishtalmut" else 0.25,
                minimal_amount_for_withdrawl=0
            )
        benjy = Parent(dict_of_monthly_incomes={"main_job": benjy_job}, dict_of_portfolios=benjy_dict_of_portfolios)


        # create inbar
        inbar_job = Job(base_salary_after_taxes=16.7, 
                probability_of_loosing_job=0.2, 
                percentage_of_base_salary_for_stocks=0.1, 
                bonus_fraction_of_annual_income=0.1, 
                dollar_amount_per_year=30,
                has_pension_plan=True,
                has_keren_hishtalmut_plan=True,

            )
        inbar_dict_of_portfolios = {NAME_OF_MAIN_PORTFOLION: PortFolio(amount_invested=40)}
        for portfolio_name in JOB_RELATED_PORTFOLIOS:
            inbar_dict_of_portfolios[portfolio_name] = PortFolio(
                amount_invested=0, 
                tax_rate_for_selling_stock=0 if portfolio_name == "keren_hishtalmut" else 0.25,
                minimal_amount_for_withdrawl=0
            )
        inbar = Parent(dict_of_monthly_incomes={"main_job": inbar_job}, dict_of_portfolios=inbar_dict_of_portfolios)


        # combine all income sources into a total incomes class
        total_incomes = TotalIncomes(dict_of_parents={"benjy": benjy, "inbar": inbar})

        return total_incomes


    def get_initial_expenses(self):
        dict_of_expenses = {
            "apartment": LocationDependentApartment(location="israel", num_kids=0),
            "bills": Bills(),
            "fun": Fun(),
            "pet": Pet(),
            "living_expenses": LivingExpenses(),
            "car": Car(payed_down_payment=True),
            "big_family_trip": BigFamilyTrip(num_days=7, num_kids=0),
            "small_family_trip1": SmallFamilyTrip(num_days=4, num_kids=0),
            "weekend_trips1": WeekendTrips(num_days=2, num_kids=0),
            "weekend_trips2": WeekendTrips(num_days=2, num_kids=0),
            "weekend_trips3": WeekendTrips(num_days=2, num_kids=0),
            "weekend_trips4": WeekendTrips(num_days=2, num_kids=0),
        }
        total_expenses = TotalExpenses(dict_of_expenses=dict_of_expenses)
        return total_expenses





    def handle_incomes_and_expenses(self, monthly_incomes, monthly_expenses):
        # handle incomes and expenses
        remaining_cash = (monthly_incomes - monthly_expenses)
        self.balance_in_bank_account += remaining_cash

        # invest or withdraw the remainder
        for parent_name in NAMES_OF_PARENTS:
            if remaining_cash > 0:
                amount_to_invest = remaining_cash/2
                self.total_incomes.invest_in_main_portfolio(parent_name, investment=amount_to_invest)
                self.balance_in_bank_account -= amount_to_invest
            else:
                amount_to_withdraw = abs(remaining_cash/2)
                amount_to_withdraw = self.total_incomes.withdraw_from_main_portfolio(parent_name, amount_to_withdraw=amount_to_withdraw)       # this is for equal withdraw which is probablly NOT the best strategy
                self.balance_in_bank_account += amount_to_withdraw

        if self.balance_in_bank_account < -10:
            raise ValueError("Bank account balance out of bounds")

        # collect portfolio values
        all_portfolios = self.total_incomes.get_portfolios()
        if self.portfolio_tracker is None:
            self.portfolio_tracker = PortFolioTracker(all_portfolios)
        else:
            self.portfolio_tracker.add_new_values_of_portfolios(all_portfolios)

        # return total_incomes, balance_in_bank_account, portfolio_tracker



    def simulate_one_year(self):
        # TODO convert to class and then we won't need all these input arguments
        for month in range(12):

            # get incomes and expenses
            monthly_incomes = self.total_incomes.get_monthly_incomes()
            monthly_expenses = self.total_expenses.get_monthly_expenses()

            # handle expenses
            self.handle_incomes_and_expenses(monthly_incomes, monthly_expenses)

            # increment month
            self.total_incomes.increment_by_one_month()
            self.total_num_months += 1

        # increment one year
        self.total_incomes.increment_by_one_year()
        self.total_expenses.increment_by_one_year() 

        # return total_incomes, self.total_expenses, balance_in_bank_account, portfolio_tracker, total_num_months


    def run_simulation(self, number_of_repititions=1):
        for year in range(self.num_years):
        
            # simulate one year
            self.simulate_one_year()

            # # apply changes if needed, according to timeline
            # self.change_incomes_if_needed()
            # self.change_expenses_if_needed()

            # self.change_jobs_if_needed()
            # self.change_country_if_needed()
           
            if year == 2:
                self.total_expenses.have_kid(location="israel")
            if year == 5:
                self.total_expenses.have_kid(location="israel")
                self.total_expenses.add_expense(expense_name="house", expense=House(full_price=3000, down_payment=600, monthly_payment=8))
                self.total_expenses.remove_expense("apartment")
            if year == 8:
                self.total_expenses.have_kid(location="israel")
            if year == 20:
                self.total_expenses.remove_expense("big_family_trip")



    def plot_all_portfolios(self):
        self.portfolio_tracker.plot_all_portfolios(self.total_num_months, target_net_worth_for_retirement=3000)