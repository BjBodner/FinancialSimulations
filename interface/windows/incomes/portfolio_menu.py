import pygame
import pygame_menu
from datetime import datetime
# from functools import part

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]


def portfolio_menu():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)

    menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Portfolio", theme=pygame_menu.themes.THEME_BLUE)

    portfolio_type = "main_portfolio" # get this as input and change it if needed

    # set defaults
    number = 1 # get this from menu constructor
    default_name = f"{portfolio_type}{number}" # get this as input based on the number of vacations already available
    default_portfolio_type = portfolio_type
    default_amount_invested = "100"
    default_minimal_amount_for_withdrawl =  "50"



    expense_dict = {"name": "", "portfolio_params": {}}

    portfolio_type_2_int = {"main_portfolio": 0}
    # fill in initial values - or get from constructor
    expense_dict["name"] = default_name
    expense_dict["portfolio_params"]["portfolio_type"] = default_portfolio_type
    expense_dict["portfolio_params"]["amount_invested"] = float(default_amount_invested)
    expense_dict["portfolio_params"]["minimal_amount_for_withdrawl"] = float(default_minimal_amount_for_withdrawl)


    # all local methods
    def process_name(name: str):
        expense_dict["name"] = name
        
    # def process_base_salary_after_taxes(base_salary_after_taxes: str):
    #     expense_dict["job_params"]["base_salary_after_taxes"] = int(base_salary_after_taxes) if len(base_salary_after_taxes) > 0 else 0

    # def process_probability_of_loosing_job(probability_of_loosing_job: str):
    #     expense_dict["job_params"]["probability_of_loosing_job"] = float(probability_of_loosing_job) if len(probability_of_loosing_job) > 0 else 0

    # def process_percentage_of_base_salary_for_stocks(percentage_of_base_salary_for_stocks: str):
    #     expense_dict["job_params"]["percentage_of_base_salary_for_stocks"] = float(percentage_of_base_salary_for_stocks) if len(percentage_of_base_salary_for_stocks) > 0 else 0

    # def process_bonus_fraction_of_annual_income(bonus_fraction_of_annual_income: str):
    #     expense_dict["job_params"]["probability_of_loosing_job"] = float(bonus_fraction_of_annual_income) if len(bonus_fraction_of_annual_income) > 0 else 0

    def process_portfolio_type(portfolio_type):
        expense_dict["portfolio_params"]["portfolio_type"] = portfolio_type

    def process_amount_invested(amount_invested: str):
        expense_dict["portfolio_params"]["amount_invested"] = float(amount_invested) if len(amount_invested) > 0 else 0

    def process_minimal_amount_for_withdrawl(minimal_amount_for_withdrawl: str):
        expense_dict["portfolio_params"]["minimal_amount_for_withdrawl"] = float(minimal_amount_for_withdrawl) if len(minimal_amount_for_withdrawl) > 0 else 0


    # def process_has_keren_hishtalmut_plan(has_keren_hishtalmut_plan):
    #     expense_dict["job_params"]["has_keren_hishtalmut_plan"] = has_keren_hishtalmut_plan

    def start_the_game():
        # Add here a function to write the expese dict to the global config
        print(expense_dict)
        print("add the expense to the config and save it")

    # add all widgets to fill in expense
    menu.add_text_input("Name: ", default=default_name, onchange=process_name, font_size=24)
    menu.add_selector(
        "portfolio_type : ", 
        default=portfolio_type_2_int[default_portfolio_type], 
        items=[("main_portfolio",), ("keren_hishtalmut",), ("pension",), ("company_stock",), ("options",)], 
        onchange=process_portfolio_type, 
        font_size=24
    )

    menu.add_text_input("amount_invested : ", default=default_amount_invested, onchange=process_amount_invested, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    menu.add_text_input("minimal_amount_for_withdrawl : ", default=default_minimal_amount_for_withdrawl, onchange=process_minimal_amount_for_withdrawl, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    # menu.add_text_input("percentage_of_base_salary_for_stocks : ", default=default_percentage_of_base_salary_for_stocks, onchange=process_percentage_of_base_salary_for_stocks, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    # menu.add_text_input("bonus_fraction_of_annual_income : ", default=default_bonus_fraction_of_annual_income, onchange=process_bonus_fraction_of_annual_income, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    # menu.add_text_input("options_per_year : ", default=default_options_per_year, onchange=process_options_per_year, valid_chars=VALID_FLOAT_CHARS, font_size=24)


    # menu.add_selector("has_keren_hishtalmut_plan : ", default=default_has_keren_hishtalmut_plan, items=[("True",), ("False",)], onchange=process_has_keren_hishtalmut_plan, font_size=24)

    # other buttons
    menu.add_vertical_margin(20)
    menu.add_button("Add Portfolio", start_the_game, font_size=24, font_color=(0,0,0))
    menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))
    menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

    menu.mainloop(surface)


if __name__ == "__main__":
    portfolio_menu()