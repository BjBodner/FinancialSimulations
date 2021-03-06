import numpy as np
import matplotlib.pyplot as plt
import yaml

import expenses
import incomes
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
from utils import NAME_OF_MAIN_PORTFOLION, JOB_RELATED_PORTFOLIOS, NAMES_OF_PARENTS, PortFolioTracker, MultiRunTracker

# TODO implement changes to country
# TODO implement changing jobs
# TODO add incomes
# TODO enable loosing after x years
# TODO enable saving yaml files for comparison
# TODO change to display only one plot at a time - the net worth


class FinancialSimulator:

    def __init__(self, config_path):
        self.config = self.load_config(config_path)

        self.total_num_months = 0 

        self.current_repetition = None

        # parse config
        self.balance_in_bank_account = self.config["simulation_params"]["balance_in_bank_account"]  # TODO load this from the config
        self.num_years = self.config["simulation_params"]["num_years"] 
        self.number_of_repetitions = self.config["simulation_params"]["number_of_repetitions"]
        self.names_of_parents = self.config["simulation_params"]["names_of_parents"]
        self.location = self.config["initial"]["location"]
        self.num_kids = self.config["initial"]["num_kids"]

        # initialize incomes and expenses
        self.total_incomes = self.get_initial_incomes()
        self.total_expenses = self.get_initial_expenses()
        self.portfolio_tracker = MultiRunTracker(self.number_of_repetitions)

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
     
        initial_expenses = self.config["initial"]["expenses"]
        dict_of_expenses = {}
        if initial_expenses is not None:
            for expense_name, expense_params in initial_expenses.items():
                    expense_class = getattr(expenses, expense_params["expense_type"])
                    dict_of_expenses[expense_name] = expense_class(**expense_params["expense_params"])

        total_expenses = TotalExpenses(dict_of_expenses=dict_of_expenses)

        return total_expenses


    def handle_incomes_and_expenses(self, monthly_incomes, monthly_expenses):
        # handle incomes and expenses
        remaining_cash = (monthly_incomes - monthly_expenses)
        self.balance_in_bank_account += remaining_cash

        # invest or withdraw the remainder
        for parent_name in self.names_of_parents:
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
        self.portfolio_tracker.add_new_values_of_portfolios(all_portfolios, self.current_repetition)
        # if self.portfolio_tracker.exists(self.current_repetition) is None:
        #     self.create_new_tracker(self.current_repetition)
        #     # self.portfolio_tracker[self.current_repetition] = PortFolioTracker(all_portfolios)
        # else:
        #     self.portfolio_tracker[self.current_repetition].add_new_values_of_portfolios(all_portfolios)


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



    def apply_changes_if_needed(self, current_year):
        # TODO convert the changes to the following format
        self.change_incomes_if_needed(current_year)
        self.change_expenses_if_needed(current_year)

        self.change_jobs_if_needed(current_year)
        self.change_country_if_needed(current_year)
        

    def change_incomes_if_needed(self, current_year):
        pass


    def change_expenses_if_needed(self, current_year):
        for expense_change_name, expense_change_information in self.config["expenses_timeline"].items():
            if expense_change_information["year"] == current_year:
                method_name = expense_change_information["method"]
                change_method = getattr(self.total_expenses, method_name)

                # implement the change
                if method_name == "add_expense":
                    params = expense_change_information["params"]
                    expense_class = getattr(expenses, params["expense_type"])
                    change_method(expense_name=params["expense_name"], expense=expense_class(**params["expense_params"]))
                else:
                    change_method(**expense_change_information["params"])
                        

    def change_jobs_if_needed(self, current_year):
        pass


    def change_country_if_needed(self, current_year):
        pass


    def run_simulation(self):

        for current_repetition in range(self.number_of_repetitions):

            # initialize incomes and expenses
            self.current_repetition = current_repetition
            self.total_incomes = self.get_initial_incomes()
            self.total_expenses = self.get_initial_expenses()
            self.total_num_months = 0
            for current_year in range(self.num_years):
            
                # simulate one year and apply any changes if needed
                self.simulate_one_year()
                self.apply_changes_if_needed(current_year)


    def plot_all_portfolios(self):
        self.portfolio_tracker.plot_all_portfolios(self.total_num_months, target_net_worth_for_retirement=3000)


    def plot_portfolio(self, portfolio_name):
        self.portfolio_tracker.plot_portfolio(self.total_num_months, portfolio_name, target_net_worth_for_retirement=3000)