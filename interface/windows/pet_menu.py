import pygame
import pygame_menu
from datetime import datetime
# from functools import part

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]


def vacation_menu():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)

    menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Pet", theme=pygame_menu.themes.THEME_BLUE)

    number = 1 # get this from menu constructor
    default_name = f"pet{number}" # get this as input based on the number of vacations already available

    expense_dict = {"name": "", "expense_params": {}, "expense_type": "Car"}

    # fill in initial values - or get from constructor
    expense_dict["name"] = default_name
    expense_dict["expense_params"]["none"] = "none"

    # # all local methods
    def process_name(name: str):
        expense_dict["name"] = name
        
    # def process_average_car_price(average_car_price: str):
    #     expense_dict["expense_params"]["average_car_price"] = int(average_car_price) if len(average_car_price) > 0 else 0

    # def process_payed_down_payment(payed_down_payment):
    #     expense_dict["expense_params"]["payed_down_payment"] = payed_down_payment

    # def process_starting_age_of_initial_car(starting_age_of_initial_car: str):
    #     expense_dict["expense_params"]["cost_per_day_per_person"] = float(starting_age_of_initial_car) if len(starting_age_of_initial_car) > 0 else 0

    # def process_average_car_lifetime(average_car_lifetime: str):
    #     expense_dict["expense_params"]["average_car_lifetime"] = float(average_car_lifetime) if len(average_car_lifetime) > 0 else 0

    def start_the_game():
        # Add here a function to write the expese dict to the global config
        print(expense_dict)
        print("add the expense to the config and save it")

    # add all widgets to fill in expense
    menu.add_text_input("Name: ", default=default_name, onchange=process_name)
    # menu.add_text_input("average_car_price : ", default=default_average_price, onchange=process_average_car_price, valid_chars=VALID_INT_CHARS)
    # menu.add_selector("payed_down_payment : ", [("True",), ("False",)], onchange=process_payed_down_payment)
    # menu.add_text_input("starting_age_of_initial_car : ", default=default_starting_age_of_initial_car, onchange=process_starting_age_of_initial_car, valid_chars=VALID_INT_CHARS)
    # menu.add_text_input("process_average_car_lifetime : ", default=default_average_car_lifetime, onchange=process_average_car_lifetime, valid_chars=VALID_FLOAT_CHARS)

    # other buttons
    menu.add_vertical_margin(40)
    menu.add_button("Add Expense", start_the_game, font_size=24, font_color=(0,0,0))
    menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))
    menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

    menu.mainloop(surface)


if __name__ == "__main__":
    vacation_menu()