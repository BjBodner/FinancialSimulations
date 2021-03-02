import pygame
import pygame_menu
# from functools import part

SURFACE_SIZE = (800, 500)
MENU_SIZE = (500, 600)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]
DEFAULT_COST_PER_DAY_PER_PERSON = {"weekend": 0.4, "small": 0.4, "big": 0.6}
FLIGHTS_PER_PERSON = {"weekend": 0, "small": 1, "big": 3}


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
    if expense_dict["name"] == "":
        print(f"highlight the name button to ask the user to fill it in")

    print(expense_dict)
    print("add the expense to the config and save it")


def vacation_menu():
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)

    menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "vacation", theme=pygame_menu.themes.THEME_BLUE)

    vacation_number = 1
    vacation_type = "weekend"

    expense_dict = {"name": "", "expense_params": {}, "expense_type": "FamilyTrip"}


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
        if expense_dict["name"] == "":
            print(f"no name selected highlight the name button to ask the user to fill it in")

        print(expense_dict)
        print("add the expense to the config and save it")


    # add all widgets to fill in expense
    menu.add_text_input("Name : ", default=f"-", onchange=process_name)
    menu.add_selector("Vacation type : ", [("weekend",), ("small",) , ("big",)], onchange=change_vacation_type)
    menu.add_text_input("Number of days : ", default="0", onchange=process_num_days, valid_chars=VALID_INT_CHARS)
    menu.add_text_input("Number of kids : ", default="0", onchange=process_num_kids, valid_chars=VALID_INT_CHARS)
    menu.add_text_input("Cost per person per day: ", default=DEFAULT_COST_PER_DAY_PER_PERSON[vacation_type], onchange=process_cost_per_day_per_person, valid_chars=VALID_FLOAT_CHARS)
    menu.add_text_input("Cost of flights per person : ", default=FLIGHTS_PER_PERSON[vacation_type], onchange=process_flights_per_person, valid_chars=VALID_FLOAT_CHARS)

    # other buttons
    menu.add_vertical_margin(40)
    menu.add_button("Add Expense", start_the_game)
    menu.add_button("Back", pygame_menu.events.BACK)
    menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT)

    menu.mainloop(surface)


if __name__ == "__main__":
    # pygame.init()
    # surface = pygame.display.set_mode(SURFACE_SIZE)

    # menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "vacation", theme=pygame_menu.themes.THEME_BLUE)

    # vacation_number = 1
    # vacation_type = "weekend"

    # expense_dict = {"name": "", "expense_params": {}, "expense_type": "FamilyTrip"}


    # # add all widgets to fill in expense
    # menu.add_text_input("Name : ", default=f"-", onchange=process_name)
    # menu.add_selector("Vacation type : ", [("weekend",), ("small",) , ("big",)], onchange=change_vacation_type)
    # menu.add_text_input("Number of days : ", default="0", onchange=process_num_days, valid_chars=VALID_INT_CHARS)
    # menu.add_text_input("Number of kids : ", default="0", onchange=process_num_kids, valid_chars=VALID_INT_CHARS)
    # menu.add_text_input("Cost per person per day: ", default=DEFAULT_COST_PER_DAY_PER_PERSON[vacation_type], onchange=process_cost_per_day_per_person, valid_chars=VALID_FLOAT_CHARS)
    # menu.add_text_input("Cost of flights per person : ", default=FLIGHTS_PER_PERSON[vacation_type], onchange=process_flights_per_person, valid_chars=VALID_FLOAT_CHARS)

    # # other buttons
    # menu.add_vertical_margin(40)
    # menu.add_button("Add Expense", start_the_game)
    # menu.add_button("Back", pygame_menu.events.BACK)
    # menu.add_button("quit", pygame_menu.events.PYGAME_QUIT)

    # menu.mainloop(surface)

    vacation_menu()