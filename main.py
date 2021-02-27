import numpy as np
import matplotlib.pyplot as plt

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


def get_total_incomes():

    # create benjy
    benjy_job = Job(base_salary_after_taxes=18.5, 
            probability_of_loosing_job=0.2, 
            percentage_of_base_salary_for_stocks=0.0, 
            bonus_fraction_of_annual_income=0.0, 
            dollar_amount_per_year=0,
            has_pension_plan=True,
            has_keren_hishtalmut_plan=True,
            phd=False, 
            mba=False, 
        )
    benjy_dict_of_portfolios = {NAME_OF_MAIN_PORTFOLION: PortFolio(amount_invested=100)}
    for portfolio_name in JOB_RELATED_PORTFOLIOS:
        benjy_dict_of_portfolios[portfolio_name] = PortFolio(
            amount_invested=0, 
            tax_rate_for_selling_stock=0 if portfolio_name == "keren_hishtalmut" else 0.25
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
            phd=False, 
            mba=False, 
        )
    inbar_dict_of_portfolios = {NAME_OF_MAIN_PORTFOLION: PortFolio(amount_invested=40)}
    for portfolio_name in JOB_RELATED_PORTFOLIOS:
        inbar_dict_of_portfolios[portfolio_name] = PortFolio(amount_invested=0)

    inbar = Parent(dict_of_monthly_incomes={"main_job": inbar_job}, dict_of_portfolios=inbar_dict_of_portfolios)

    # combine all income sources
    total_incomes = TotalIncomes(dict_of_parents={"benjy": benjy, "inbar": inbar})

    return total_incomes

def get_total_expenses():
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



def handle_incomes_and_expenses(monthly_incomes, monthly_expenses, total_incomes, balance_in_bank_account, portfolio_tracker):
    # handle incomes and expenses
    remaining_cash = (monthly_incomes - monthly_expenses)
    balance_in_bank_account += remaining_cash

    # invest or withdraw the remainder
    for parent_name in NAMES_OF_PARENTS:
        if remaining_cash > 0:
            amount_to_invest = remaining_cash/2
            total_incomes.invest_in_main_portfolio(parent_name, investment=amount_to_invest)
            balance_in_bank_account -= amount_to_invest
        else:
            amount_to_withdraw = abs(remaining_cash/2)
            amount_to_withdraw = total_incomes.withdraw_from_main_portfolio(parent_name, amount_to_withdraw=amount_to_withdraw)       # this is for equal withdraw which is probablly NOT the best strategy
            balance_in_bank_account += amount_to_withdraw

    if balance_in_bank_account < -10:
        raise ValueError("Bank account balance out of bounds")

    # collect portfolio values
    all_portfolios = total_incomes.get_portfolios()
    if portfolio_tracker is None:
        portfolio_tracker = PortFolioTracker(all_portfolios)
    else:
        portfolio_tracker.add_new_values_of_portfolios(all_portfolios)

    return total_incomes, balance_in_bank_account, portfolio_tracker


def simulate_one_year(total_incomes, total_expenses, balance_in_bank_account, portfolio_tracker, total_num_months):
    # TODO convert to class and then we won't need all these input arguments
    for month in range(12):

        # get incomes and expenses
        monthly_incomes = total_incomes.get_monthly_incomes()
        monthly_expenses = total_expenses.get_monthly_expenses()

        # handle expenses
        total_incomes, balance_in_bank_account, portfolio_tracker = handle_incomes_and_expenses(monthly_incomes, monthly_expenses, total_incomes, balance_in_bank_account, portfolio_tracker)

        # increment month
        total_incomes.increment_by_one_month()
        total_num_months += 1

    # increment one year
    total_incomes.increment_by_one_year()
    total_expenses.increment_by_one_year() 

    return total_incomes, total_expenses, balance_in_bank_account, portfolio_tracker, total_num_months


if __name__ == "__main__":
    total_incomes = get_total_incomes()
    total_expenses = get_total_expenses()

    total_num_months = 0
    balance_in_bank_account = 0
    num_years = 35
    portfolio_tracker = None 

    for year in range(num_years):
       
        # simulate one year
        total_incomes, total_expenses, balance_in_bank_account, portfolio_tracker, total_num_months = simulate_one_year(total_incomes, total_expenses, balance_in_bank_account, portfolio_tracker, total_num_months)

        # timeline 
        # TODO make the timeline more easily managable, and make it available to save as a file
        # TODO add a change location operation
        # TODO add a change jobs operation
        if year == 2:
            total_expenses.have_kid(location="israel")
        if year == 5:
            total_expenses.have_kid(location="israel")
            total_expenses.add_expense(expense_name="house", expense=House(full_price=3000, down_payment=600, monthly_payment=8))
            total_expenses.remove_expense("apartment")
        if year == 8:
            total_expenses.have_kid(location="israel")
        if year == 20:
            total_expenses.remove_expense("big_family_trip")


    # plot portfolios
    # TODO make comparisons easily available
    portfolio_tracker.plot_all_portfolios(total_num_months, target_net_worth_for_retirement=3000)