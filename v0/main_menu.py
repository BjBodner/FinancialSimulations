import pygame
import pygame_menu
from datetime import datetime
from functools import partial
import yaml
import copy

SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]

TEMPLATE_JOB_PATH = "configs\template_job.yaml"
with open(TEMPLATE_JOB_PATH, "r") as fh:
    TEMPLATE_JOB = yaml.load(fh, yaml.FullLoader)


class JobMenu:

    def __init__(self, name, global_config):
            
        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], name, theme=pygame_menu.themes.THEME_BLUE)
        self.global_config = global_config

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


        self.job_dict = {"name": "", "job_params": {}}

        # fill in initial values - or get from constructor
        self.job_dict["name"] = default_name
        self.job_dict["job_params"]["base_salary_after_taxes"] = default_base_salary_after_taxes
        self.job_dict["job_params"]["probability_of_loosing_job"] = default_probability_of_loosing_job
        self.job_dict["job_params"]["percentage_of_base_salary_for_stocks"] = default_percentage_of_base_salary_for_stocks
        self.job_dict["job_params"]["bonus_fraction_of_annual_income"] = default_bonus_fraction_of_annual_income
        self.job_dict["job_params"]["options_per_year"] = default_options_per_year
        self.job_dict["job_params"]["has_pension_plan"] = default_has_pension_plan
        self.job_dict["job_params"]["has_keren_hishtalmut_plan"] = default_has_keren_hishtalmut_plan

        # add all widgets to fill in expense
        self.menu.add_text_input("Name: ", default=default_name, onchange=self.process_name, font_size=38)
        self.name_widget = self.menu.get_widgets()[-1]
        self.menu.add_text_input("base_salary_after_taxes : ", default=default_base_salary_after_taxes, onchange=self.process_base_salary_after_taxes, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_text_input("probability_of_loosing_job : ", default=default_probability_of_loosing_job, onchange=self.process_probability_of_loosing_job, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_text_input("percentage_of_base_salary_for_stocks : ", default=default_percentage_of_base_salary_for_stocks, onchange=self.process_percentage_of_base_salary_for_stocks, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_text_input("bonus_fraction_of_annual_income : ", default=default_bonus_fraction_of_annual_income, onchange=self.process_bonus_fraction_of_annual_income, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_text_input("options_per_year : ", default=default_options_per_year, onchange=self.process_options_per_year, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_selector("has_pension_plan : ", default=default_has_pension_plan, items=[("True",), ("False",)], onchange=self.process_has_pension_plan, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_selector("has_keren_hishtalmut_plan : ", default=default_has_keren_hishtalmut_plan, items=[("True",), ("False",)], onchange=self.process_has_keren_hishtalmut_plan, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)

        # other buttons
        self.menu.add_vertical_margin(20)
        self.menu.add_button("Add Income", self.add_income, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))

        # all local methods
    def process_name(self, name: str):
        self.job_dict["name"] = name
        
    def process_base_salary_after_taxes(self, base_salary_after_taxes: str):
        self.job_dict["job_params"]["base_salary_after_taxes"] = int(base_salary_after_taxes) if len(base_salary_after_taxes) > 0 else 0

    def process_probability_of_loosing_job(self, probability_of_loosing_job: str):
        self.job_dict["job_params"]["probability_of_loosing_job"] = float(probability_of_loosing_job) if len(probability_of_loosing_job) > 0 else 0

    def process_percentage_of_base_salary_for_stocks(self, percentage_of_base_salary_for_stocks: str):
        self.job_dict["job_params"]["percentage_of_base_salary_for_stocks"] = float(percentage_of_base_salary_for_stocks) if len(percentage_of_base_salary_for_stocks) > 0 else 0

    def process_bonus_fraction_of_annual_income(self, bonus_fraction_of_annual_income: str):
        self.job_dict["job_params"]["probability_of_loosing_job"] = float(bonus_fraction_of_annual_income) if len(bonus_fraction_of_annual_income) > 0 else 0

    def process_options_per_year(self, options_per_year: str):
        self.job_dict["job_params"]["options_per_year"] = float(options_per_year) if len(options_per_year) > 0 else 0

    def process_has_pension_plan(self, has_pension_plan):
        self.job_dict["job_params"]["has_pension_plan"] = has_pension_plan

    def process_has_keren_hishtalmut_plan(self, has_keren_hishtalmut_plan):
        self.job_dict["job_params"]["has_keren_hishtalmut_plan"] = has_keren_hishtalmut_plan

    def add_income(self):
        # Add here a function to write the expese dict to the global config
        print(self.job_dict)
        print("add the expense to the config and save it")
        # add the income to the config of all the saved incomes - the name is the job name
        name = self.job_dict["name"]
        self.global_config["initial"]["incomes"][name] = copy.deepcopy(TEMPLATE_JOB) # TODO make a template job
        self.global_config["initial"]["incomes"][name]["jobs"]["main_job"] = {**self.job_dict["job_params"]}
        print(self.global_config)



class CompareMenu:

    def __init__(self, name, global_config):

        # self.num_saved_offers = 10
        # self.all_offers = [f"job{i}" for i in  range(self.num_saved_offers)]

        self.num_saved_offers = len(global_config["initial"]["incomes"])
        self.all_offers = list(global_config["initial"]["incomes"].keys())


        self.offers_to_compare = {}
        self.name_to_widget = {}
        self.num_rows_per_colum = self.num_saved_offers + 2

        self.global_config = global_config
        self.initialize_temporary_config()

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare Offers", columns=2, rows=self.num_rows_per_colum, theme=pygame_menu.themes.THEME_BLUE)
        # self.compare_offers_menu.add_label("this is the second menu")
        self.initialize_compare_offers_menu()

    def initialize_temporary_config(self):
        self.temporary_config = copy.deepcopy(self.global_config)
        self.temporary_config["initial"]["incomes"] = {}


    def add_offer_to_compare_list(self, offer_name):
        # adds an offer to the compare list
        if offer_name not in self.name_to_widget.keys():
            # self.offers_to_compare[]offer_name)
            self.menu.add_button(offer_name, partial(self.remove_offer_from_compare_list, offer_name), align=pygame_menu.locals.ALIGN_RIGHT, 
            font_size=20, font_color=(0,0,0),
            # widget_id=widget_id
            )
            self.name_to_widget[offer_name] = self.menu.get_widgets()[-1]

            # TODO add the details of the config we selected to a temporary config we will run
            self.temporary_config["initial"]["incomes"][offer_name] = copy.deepcopy(self.global_config["initial"]["incomes"][offer_name])
            

    def remove_offer_from_compare_list(self, offer_name):
        # removes an offer from the compare list
        self.menu.remove_widget(self.name_to_widget[offer_name])
        self.name_to_widget.pop(offer_name)
        self.temporary_config["initial"]["incomes"].pop(offer_name)

    def initialize_compare_offers_menu(self):
        self.menu.clear()
        self.menu.add_label("Add offers to compare", align=pygame_menu.locals.ALIGN_LEFT, font_size=24, font_color=(0,0,0))

        # add all the options to select
        self.menu.add_vertical_margin(10)
        for offer_name in self.all_offers:
            self.menu.add_button(offer_name, partial(self.add_offer_to_compare_list, offer_name), align=pygame_menu.locals.ALIGN_LEFT, font_size=20, font_color=(0,0,0))

        # add the second column
        self.menu.add_button("Compare", self.compare_offers, align=pygame_menu.locals.ALIGN_TOP, font_size=24, 
            font_color=(0,0,210), 
            background_color=(200, 200, 255),
        )
        self.menu.add_vertical_margin(10)


    def compare_offers(self):
        # TODO
        # save the temprary config to file
        # run the main algorithm with the temprary config
        # save the plot to a place
        # display the image in the menu

        print(f"do comparison")



class MainMenu:

    def __init__(self, surface, number=1, name=None, theme=pygame_menu.themes.THEME_BLUE, config_file="configs\job_only_config.yaml"):

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare offerings", theme=theme)

        # remove this - this is just to demonstrate how to add multiple menus
        # self.menu2 = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Bills2", theme=pygame_menu.themes.THEME_BLUE)
        # self.menu2.add_label("this is the second menu")

        self.config = self.load_config(config_file)

        self.add_offer_menu = JobMenu("Add Offer", self.config)
        self.compare_offers_menu = CompareMenu("Compare Offers", self.config)
        self.edit_income_handling_menu = CompareMenu("Compare Offers", self.config) # for this just use a fixed expense type



        # add_job_funcitonallity(self.new_offer_menu)
        # self.new_offer_menu = job_menu()
        # self.new_offer_menu.add_label("this is the second menu")


        # self.num_saved_offers = 10
        # self.all_offers = [f"job{i}" for i in  range(self.num_saved_offers)]
        # self.offers_to_compare = []
        # self.name_to_widget = {}
        # self.num_rows_per_colum = self.num_saved_offers + 2
        # self.compare_offers_menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare Offers", columns=2, rows=self.num_rows_per_colum, theme=pygame_menu.themes.THEME_BLUE)
        # # self.compare_offers_menu.add_label("this is the second menu")
        # self.initialize_compare_offers_menu()


        # set defaults from the constructor
        self.default_name = name if name is not None else f"bills{number}"

        # self.initialize_expense_dict()
        self.add_parameter_buttons_and_fields()
        self.add_navigation_buttons()

    def load_config(self, config_file):
        with open(config_file, "r") as fh:
            return yaml.load(fh, yaml.FullLoader)


    def add_parameter_buttons_and_fields(self):
        # add parameter buttons and fields
        # self.menu.add_text_input("Name: ", default=self.default_name, onchange=self.process_name)
        self.menu.add_button("Edit Income Handling", self.edit_income_handling_menu.menu, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Add Offer", self.add_offer_menu.menu, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Compare Offers", self.compare_offers_menu.menu, font_size=24, font_color=(0,0,0))
        


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
    MainMenu(surface, number=1).run()