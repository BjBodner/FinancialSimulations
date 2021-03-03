import pygame
import pygame_menu
from datetime import datetime
# from functools import part

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]


class BillsMenu:

    def __init__(self, surface, number=1, name=None, theme=pygame_menu.themes.THEME_BLUE):

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Bills", theme=theme)

        # remove this - this is just to demonstrate how to add multiple menus
        self.menu2 = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Bills2", theme=pygame_menu.themes.THEME_BLUE)
        self.menu2.add_label("this is the second menu")

        # set defaults from the constructor
        self.default_name = name if name is not None else f"bills{number}"

        self.initialize_expense_dict()
        self.add_parameter_buttons_and_fields()
        self.add_navigation_buttons()

    def initialize_expense_dict(self):
        # initialize the expense dict
        self.expense_dict = {"name": "", "expense_params": {}, "expense_type": "Bills"}
        self.expense_dict["name"] = self.default_name
        self.expense_dict["expense_params"]["none"] = "none"

    def add_parameter_buttons_and_fields(self):
        # add parameter buttons and fields
        self.menu.add_text_input("Name: ", default=self.default_name, onchange=self.process_name)
        self.menu.add_button("menu2", self.menu2, font_size=24, font_color=(0,0,0))

    def add_navigation_buttons(self):
        # add navigation buttons
        self.menu.add_vertical_margin(40)
        self.menu.add_button("Add Expense", self.start_the_game, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

        # # all local methods
    def process_name(self, name: str):
        self.expense_dict["name"] = name
        
    def start_the_game(self):
        # Add here a function to write the expese dict to the global config
        print(self.expense_dict)
        print("add the expense to the config and save it")
        pygame_menu.events.BACK
            
    def run(self):
        self.menu.mainloop(surface)


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)
    BillsMenu(surface, number=1).run()