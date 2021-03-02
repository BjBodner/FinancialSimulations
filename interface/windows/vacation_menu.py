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

    DEFAULT_COST_PER_DAY_PER_PERSON = {"weekend": 0.4, "small": 0.4, "big": 0.6}
    FLIGHTS_PER_PERSON = {"weekend": 0, "small": 1, "big": 3}

    menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Vacation", theme=pygame_menu.themes.THEME_BLUE)

    number = 1 # get this from menu constructor
    default_name = f"vacation{number}" # get this as input based on the number of vacations already available
    vacation_type = "weekend"

    expense_dict = {"name": "", "expense_params": {}, "expense_type": "FamilyTrip"}

    # fill in initial values - or get from constructor
    expense_dict["name"] = default_name
    expense_dict["expense_params"]["num_kids"] = 0
    expense_dict["expense_params"]["num_days"] = 0
    expense_dict["expense_params"]["cost_per_day_per_person"] = DEFAULT_COST_PER_DAY_PER_PERSON[vacation_type]
    expense_dict["expense_params"]["flights_per_person"] = FLIGHTS_PER_PERSON[vacation_type]

    # all local methods
    def change_vacation_type(vacation_type_):
        vacation_type = vacation_type_

    def process_name(name: str):
        expense_dict["name"] = name
        
    def process_num_kids(num_kids: str):
        expense_dict["expense_params"]["num_kids"] = int(num_kids) if len(num_kids) > 0 else 0

    def process_num_days(num_days: str):
        expense_dict["expense_params"]["num_days"] = int(num_days) if len(num_days) > 0 else 0

    def process_cost_per_day_per_person(cost_per_day_per_person: str):
        expense_dict["expense_params"]["cost_per_day_per_person"] = float(cost_per_day_per_person) if len(cost_per_day_per_person) > 0 else 0

    def process_flights_per_person(flights_per_person: str):
        expense_dict["expense_params"]["flights_per_person"] = float(flights_per_person) if len(flights_per_person) > 0 else 0

    def start_the_game():
        # Add here a function to write the expese dict to the global config
        print(expense_dict)
        print("add the expense to the config and save it")
        pygame_menu.events.BACK
        
    # add all widgets to fill in expense
    menu.add_text_input("Name: ", default=default_name, onchange=process_name)
    menu.add_selector("Vacation type : ", [("weekend",), ("small",) , ("big",)], onchange=change_vacation_type)
    menu.add_text_input("Number of days : ", default="0", onchange=process_num_days, valid_chars=VALID_INT_CHARS)
    menu.add_text_input("Number of kids : ", default="0", onchange=process_num_kids, valid_chars=VALID_INT_CHARS)
    menu.add_text_input("Cost per person per day: ", default=DEFAULT_COST_PER_DAY_PER_PERSON[vacation_type], onchange=process_cost_per_day_per_person, valid_chars=VALID_FLOAT_CHARS)
    menu.add_text_input("Cost of flights per person : ", default=FLIGHTS_PER_PERSON[vacation_type], onchange=process_flights_per_person, valid_chars=VALID_FLOAT_CHARS)

    # other buttons
    menu.add_vertical_margin(40)
    menu.add_button("Add Expense", start_the_game, font_size=24, font_color=(0,0,0))
    menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))
    menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

    menu.mainloop(surface)


if __name__ == "__main__":
    vacation_menu()