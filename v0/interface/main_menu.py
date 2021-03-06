import pygame
import pygame_menu
from datetime import datetime
from functools import partial

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]


class BillsMenu:

    def __init__(self, surface, number=1, name=None, theme=pygame_menu.themes.THEME_BLUE):

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare offerings", theme=theme)

        # remove this - this is just to demonstrate how to add multiple menus
        # self.menu2 = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Bills2", theme=pygame_menu.themes.THEME_BLUE)
        # self.menu2.add_label("this is the second menu")


        self.new_offer_menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Add Offer", theme=pygame_menu.themes.THEME_BLUE)
        # self.new_offer_menu.add_label("this is the second menu")


        self.num_saved_offers = 10
        self.all_offers = [f"job{i}" for i in  range(self.num_saved_offers)]
        self.offers_to_compare = []
        self.name_to_id = {}
        self.num_rows_per_colum = self.num_saved_offers + 2
        self.compare_offers_menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare Offers", columns=2, rows=self.num_rows_per_colum, theme=pygame_menu.themes.THEME_BLUE)
        self.compare_offers_menu.add_label("this is the second menu")
        self.initialize_compare_offers_menu()


        # set defaults from the constructor
        self.default_name = name if name is not None else f"bills{number}"

        self.initialize_expense_dict()
        self.add_parameter_buttons_and_fields()
        self.add_navigation_buttons()


    def add_offer_to_compare_list(self, offer_name):
        if offer_name not in self.offers_to_compare:
            self.offers_to_compare.append(offer_name)
            widget_id = str(len(self.offers_to_compare))
            self.compare_offers_menu.add_button(offer_name, partial(self.remove_offer_from_compare_list, offer_name), align=pygame_menu.locals.ALIGN_RIGHT, 
            font_size=20, font_color=(0,0,0),
            widget_id=widget_id
            )
            self.name_to_id[offer_name] = widget_id

    def remove_offer_from_compare_list(self, offer_name):
        self.compare_offers_menu.remove_widget(self.name_to_id[offer_name])


        # for offer_name in self.offers_to_compare:
            # self.compare_offers_menu.add_button(offer_name, partial(self.add_offer_to_compare_list, offer_name), align=pygame_menu.locals.ALIGN_RIGHT, font_size=20, font_color=(0,0,0))

    def initialize_compare_offers_menu(self):
        self.compare_offers_menu.clear()
        self.compare_offers_menu.add_label("Add offers to compare", align=pygame_menu.locals.ALIGN_LEFT, font_size=24, font_color=(0,0,0))
        # self.compare_offers_menu.add_label("Offers to compare", align=pygame_menu.locals.ALIGN_RIGHT, font_size=24, font_color=(0,0,0))

        # padding=()
        self.compare_offers_menu.add_vertical_margin(10)
        for offer_name in self.all_offers:
            self.compare_offers_menu.add_button(offer_name, partial(self.add_offer_to_compare_list, offer_name), align=pygame_menu.locals.ALIGN_LEFT, font_size=20, font_color=(0,0,0))

        self.compare_offers_menu.add_label("Offers to compare", align=pygame_menu.locals.ALIGN_RIGHT, font_size=24, font_color=(0,0,0))
        self.compare_offers_menu.add_vertical_margin(10)

        # self.compare_offers_menu.add_selector(pygame_menu.widgets.LeftArrowSelection())

        # self.compare_offers_menu()

    def initialize_expense_dict(self):
        # initialize the expense dict
        self.expense_dict = {"name": "", "expense_params": {}, "expense_type": "Bills"}
        self.expense_dict["name"] = self.default_name
        self.expense_dict["expense_params"]["none"] = "none"

    def add_parameter_buttons_and_fields(self):
        # add parameter buttons and fields
        # self.menu.add_text_input("Name: ", default=self.default_name, onchange=self.process_name)
        self.menu.add_button("Add Offer", self.new_offer_menu, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Compare Offers", self.compare_offers_menu, font_size=24, font_color=(0,0,0))


    def add_navigation_buttons(self):
        # add navigation buttons
        self.menu.add_vertical_margin(40)
        # self.menu.add_button("Add Expense", self.start_the_game, font_size=24, font_color=(0,0,0))
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