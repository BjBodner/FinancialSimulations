import pygame
import pygame_menu
from datetime import datetime
# from functools import part

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]


def job_menu():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)

    menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Car", theme=pygame_menu.themes.THEME_BLUE)

    # set defaults
    number = 1 # get this from menu constructor
    default_name = f"job{number}" # get this as input based on the number of vacations already available
    default_base_salary_after_taxes = 18.5
    default_probability_of_loosing_job =  0.2
    default_percentage_of_base_salary_for_stocks =  0.0
    default_bonus_fraction_of_annual_income =  0.0
    default_options_per_year = 0
    default_has_pension_plan = True
    default_has_keren_hishtalmut_plan =  True


    expense_dict = {"name": "", "job_params": {}}

    # fill in initial values - or get from constructor
    expense_dict["name"] = default_name
    expense_dict["job_params"]["base_salary_after_taxes"] = default_base_salary_after_taxes
    expense_dict["job_params"]["probability_of_loosing_job"] = default_probability_of_loosing_job
    expense_dict["job_params"]["percentage_of_base_salary_for_stocks"] = default_percentage_of_base_salary_for_stocks
    expense_dict["job_params"]["bonus_fraction_of_annual_income"] = default_bonus_fraction_of_annual_income
    expense_dict["job_params"]["options_per_year"] = default_options_per_year
    expense_dict["job_params"]["has_pension_plan"] = default_has_pension_plan
    expense_dict["job_params"]["has_keren_hishtalmut_plan"] = default_has_keren_hishtalmut_plan

    # all local methods
    def process_name(name: str):
        expense_dict["name"] = name
        
    def process_base_salary_after_taxes(base_salary_after_taxes: str):
        expense_dict["job_params"]["base_salary_after_taxes"] = int(base_salary_after_taxes) if len(base_salary_after_taxes) > 0 else 0

    def process_probability_of_loosing_job(probability_of_loosing_job: str):
        expense_dict["job_params"]["probability_of_loosing_job"] = float(probability_of_loosing_job) if len(probability_of_loosing_job) > 0 else 0

    def process_percentage_of_base_salary_for_stocks(percentage_of_base_salary_for_stocks: str):
        expense_dict["job_params"]["percentage_of_base_salary_for_stocks"] = float(percentage_of_base_salary_for_stocks) if len(percentage_of_base_salary_for_stocks) > 0 else 0

    def process_bonus_fraction_of_annual_income(bonus_fraction_of_annual_income: str):
        expense_dict["job_params"]["probability_of_loosing_job"] = float(bonus_fraction_of_annual_income) if len(bonus_fraction_of_annual_income) > 0 else 0

    def process_options_per_year(options_per_year: str):
        expense_dict["job_params"]["options_per_year"] = float(options_per_year) if len(options_per_year) > 0 else 0

    def process_has_pension_plan(has_pension_plan):
        expense_dict["job_params"]["has_pension_plan"] = has_pension_plan

    def process_has_keren_hishtalmut_plan(has_keren_hishtalmut_plan):
        expense_dict["job_params"]["has_keren_hishtalmut_plan"] = has_keren_hishtalmut_plan

    def start_the_game():
        # Add here a function to write the expese dict to the global config
        print(expense_dict)
        print("add the expense to the config and save it")

    # add all widgets to fill in expense
    menu.add_text_input("Name: ", default=default_name, onchange=process_name, font_size=24)
    menu.add_text_input("base_salary_after_taxes : ", default=default_base_salary_after_taxes, onchange=process_base_salary_after_taxes, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    menu.add_text_input("probability_of_loosing_job : ", default=default_probability_of_loosing_job, onchange=process_probability_of_loosing_job, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    menu.add_text_input("percentage_of_base_salary_for_stocks : ", default=default_percentage_of_base_salary_for_stocks, onchange=process_percentage_of_base_salary_for_stocks, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    menu.add_text_input("bonus_fraction_of_annual_income : ", default=default_bonus_fraction_of_annual_income, onchange=process_bonus_fraction_of_annual_income, valid_chars=VALID_FLOAT_CHARS, font_size=24)
    menu.add_text_input("options_per_year : ", default=default_options_per_year, onchange=process_options_per_year, valid_chars=VALID_FLOAT_CHARS, font_size=24)


    menu.add_selector("has_pension_plan : ", default=default_has_pension_plan, items=[("True",), ("False",)], onchange=process_has_pension_plan, font_size=24)
    menu.add_selector("has_keren_hishtalmut_plan : ", default=default_has_keren_hishtalmut_plan, items=[("True",), ("False",)], onchange=process_has_keren_hishtalmut_plan, font_size=24)

    # other buttons
    menu.add_vertical_margin(20)
    menu.add_button("Add Income", start_the_game, font_size=24, font_color=(0,0,0))
    menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))
    menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

    menu.mainloop(surface)


if __name__ == "__main__":
    job_menu()