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

# TODO add multiple runs for averaging and variance analysis


class FinancialSimulator:

    def __init__(self, config_path):
        self.config = self.load_config(config_path)

        self.total_num_months = 0 
        self.portfolio_tracker = None

        # parse config
        self.balance_in_bank_account = self.config["simulation_params"]["balance_in_bank_account"]  # TODO load this from the config
        self.num_years = self.config["simulation_params"]["num_years"] 
        self.names_of_parents = self.config["simulation_params"]["names_of_parents"]
        self.location = self.config["initial"]["location"]
        self.num_kids = self.config["initial"]["num_kids"]
        
        # initialize incomes and expenses
        self.total_incomes = self.get_initial_incomes()
        self.total_expenses = self.get_initial_expenses()


    def load_config(self, config_path):
        with open(config_path, "r") as fh:
            return yaml.load(fh, yaml.FullLoader)


    def get_initial_incomes(self):

        initial_incomes_params = self.config["initial"]["incomes"]
        dict_of_parents = {}

        # create all parents
        for parent_name in self.names_of_parents:

            # create jobs
            dict_of_monthly_incomes = {"main_job": Job(**initial_incomes_params[parent_name]["jobs"]["main_job"])}

            # create portfolios
            dict_of_portfolios = {
                portfolio_name: PortFolio(**porfolio_params) for portfolio_name, porfolio_params in initial_incomes_params[parent_name]["porfolios"].items()
            }

            # create parent
            dict_of_parents[parent_name] = Parent(dict_of_monthly_incomes=dict_of_monthly_incomes, dict_of_portfolios=dict_of_portfolios)

        # combine all into total incomes
        total_incomes = TotalIncomes(dict_of_parents=dict_of_parents)

        return total_incomes


    def get_initial_expenses(self):
        dict_of_expenses = {
            "apartment": LocationDependentApartment(location=self.location, num_kids=self.num_kids),
            "bills": Bills(),
            "fun": Fun(),
            "pet": Pet(),
            "living_expenses": LivingExpenses(),
            "car": Car(payed_down_payment=True),
            "big_family_trip": BigFamilyTrip(num_days=7, num_kids=self.num_kids),
            "small_family_trip1": SmallFamilyTrip(num_days=4, num_kids=self.num_kids),
            "weekend_trips1": WeekendTrips(num_days=2, num_kids=self.num_kids),
            "weekend_trips2": WeekendTrips(num_days=2, num_kids=self.num_kids),
            "weekend_trips3": WeekendTrips(num_days=2, num_kids=self.num_kids),
            "weekend_trips4": WeekendTrips(num_days=2, num_kids=self.num_kids),
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


    def simulate_one_year(self):
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


    def run_simulation(self, number_of_repititions=1):
        for year in range(self.num_years):
        
            # simulate one year
            self.simulate_one_year()

            self.apply_changes_if_needed(year)

    def apply_changes_if_needed(self, year):
        # TODO convert the changes to the following format
        # self.change_incomes_if_needed()
        # self.change_expenses_if_needed()

        # self.change_jobs_if_needed()
        # self.change_country_if_needed()
        
        if year == 2:
            self.total_expenses.have_kid(location=self.location)
        if year == 5:
            self.total_expenses.have_kid(location=self.location)
            self.total_expenses.add_expense(expense_name="house", expense=House(full_price=3000, down_payment=600, monthly_payment=8))
            self.total_expenses.remove_expense("apartment")
        if year == 8:
            self.total_expenses.have_kid(location=self.location)
        if year == 20:
            self.total_expenses.remove_expense("big_family_trip")


    def plot_all_portfolios(self):
        self.portfolio_tracker.plot_all_portfolios(self.total_num_months, target_net_worth_for_retirement=3000)