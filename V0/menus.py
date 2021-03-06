import pygame
import pygame_menu
from datetime import datetime
from functools import partial
import yaml
import copy
import os 
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append("\\".join(os.path.dirname(__file__).split("\\")[:-1]))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from financial_simulator import FinancialSimulator


SURFACE_SIZE = (1000, 600)
MENU_SIZE = (600, 700)
VALID_FLOAT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9", "."]
VALID_INT_CHARS = ["0", "1", "2", "2", "3", "4", "5", "6", "7", "8", "9"]

TEMPLATE_JOB_PATH = r"configs\template_job.yaml"
with open(TEMPLATE_JOB_PATH, "r") as fh:
    TEMPLATE_JOB = yaml.load(fh, yaml.FullLoader)

STR_2_BOOL = {"True": True, "False": False}



class SimulationSettingsMenu:

    # TODO set up expenses
    def __init__(self, name, global_config, config_file, main_menu_object):
          
        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], name, theme=pygame_menu.themes.THEME_BLUE)

        self.global_config = global_config
        self.config_file = config_file
        self.main_menu_object = main_menu_object

        # set defaults
        default_number_of_years_to_simulate = self.global_config["simulation_params"]["num_years"]
        default_monthly_expenses = self.global_config["initial"]["expenses"]["fixed_monthly_expenses"]["expense_params"]["monthly_expense"]

        self.monthly_expenses = default_monthly_expenses
        self.number_of_years_to_simulate = default_number_of_years_to_simulate

        self.menu.add_text_input("monthly_expenses : ", default=default_monthly_expenses, onchange=self.process_monthly_expenses, valid_chars=VALID_FLOAT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)
        self.menu.add_text_input("number_of_years_to_simulate : ", default=default_number_of_years_to_simulate, onchange=self.process_number_of_years_to_simulate, valid_chars=VALID_INT_CHARS, align=pygame_menu.locals.ALIGN_LEFT, 
            font_size=20, font_color=(0,0,0),)

        # other buttons
        self.menu.add_vertical_margin(20)
        self.menu.add_button("Save Settings", self.save_settings, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Back", pygame_menu.events.BACK, font_size=24, font_color=(0,0,0))

    def process_monthly_expenses(self, monthly_expenses: str):
        self.monthly_expenses = float(monthly_expenses) if len(monthly_expenses) > 0 else 0

    def process_number_of_years_to_simulate(self, number_of_years_to_simulate: str):
        self.number_of_years_to_simulate = int(number_of_years_to_simulate) if len(number_of_years_to_simulate) > 0 else 0

    def save_settings(self):
        # Add here a function to write the expese dict to the global config
        print(f"number_of_years_to_simulate = {self.number_of_years_to_simulate}, monthly_expenses = {self.monthly_expenses}")

        with open(self.config_file, "r") as fh:
            self.global_config = yaml.load(fh, yaml.FullLoader)

        self.global_config["simulation_params"]["num_years"] = self.number_of_years_to_simulate

        self.global_config["initial"]["expenses"] = {}
        self.global_config["initial"]["expenses"]["fixed_monthly_expenses"] = {
            "expense_type" : "FixedMonthlyExpense",
            "expense_params": {"monthly_expense" : self.monthly_expenses}
        }

        # overwrite yaml file
        with open(self.config_file, "w") as fh:
            yaml.dump(self.global_config, fh)

        # printout successfullly added to global config
        self.menu.add_vertical_margin(20)
        self.menu.add_label("saved settings!", align=pygame_menu.locals.ALIGN_CENTER, font_size=30, font_color=(0,200,0))

        # reinitialize all menus
        self.reinitialize_main_menu_widgets()


    def reinitialize_main_menu_widgets(self):
        self.menu_name_to_widget = {}
        self.main_menu_object.menu.clear()
        self.main_menu_object.create_submenus()
        self.main_menu_object.add_parameter_buttons_and_fields()
        self.main_menu_object.add_navigation_buttons()


class JobMenu:

    def __init__(self, name, global_config, config_file, main_menu_object):
            
        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], name, theme=pygame_menu.themes.THEME_BLUE)
        self.compare_offers_menu = CompareMenu("Compare Offers", global_config, config_file)
        self.remove_offers_menu = RemoveMenu("Remove Offers", global_config, config_file, main_menu_object)

        self.global_config = global_config
        self.config_file = config_file
        self.main_menu_object = main_menu_object

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
        self.job_dict["job_params"]["base_salary_after_taxes"] = float(base_salary_after_taxes) if len(base_salary_after_taxes) > 0 else 0

    def process_probability_of_loosing_job(self, probability_of_loosing_job: str):
        self.job_dict["job_params"]["probability_of_loosing_job"] = float(probability_of_loosing_job) if len(probability_of_loosing_job) > 0 else 0

    def process_percentage_of_base_salary_for_stocks(self, percentage_of_base_salary_for_stocks: str):
        self.job_dict["job_params"]["percentage_of_base_salary_for_stocks"] = float(percentage_of_base_salary_for_stocks) if len(percentage_of_base_salary_for_stocks) > 0 else 0

    def process_bonus_fraction_of_annual_income(self, bonus_fraction_of_annual_income: str):
        self.job_dict["job_params"]["probability_of_loosing_job"] = float(bonus_fraction_of_annual_income) if len(bonus_fraction_of_annual_income) > 0 else 0

    def process_options_per_year(self, options_per_year: str):
        self.job_dict["job_params"]["options_per_year"] = float(options_per_year) if len(options_per_year) > 0 else 0

    def process_has_pension_plan(self, has_pension_plan):
        self.job_dict["job_params"]["has_pension_plan"] = STR_2_BOOL[has_pension_plan[0][0]]

    def process_has_keren_hishtalmut_plan(self, has_keren_hishtalmut_plan):
        self.job_dict["job_params"]["has_keren_hishtalmut_plan"] = STR_2_BOOL[has_keren_hishtalmut_plan[0][0]]

    def add_income(self):
        # Add here a function to write the expese dict to the global config
        print(self.job_dict)
        print("add the expense to the config and save it")

        # load global config
        with open(self.config_file, "r") as fh:
            self.global_config = yaml.load(fh, yaml.FullLoader)

        # add the income to the config of all the saved incomes - the name is the job name
        name = self.job_dict["name"]
        self.global_config["initial"]["incomes"][name] = copy.deepcopy(TEMPLATE_JOB)["template_job"] 
        self.global_config["initial"]["incomes"][name]["jobs"]["main_job"] = {**self.job_dict["job_params"]}
        self.global_config["simulation_params"]["names_of_parents"].append(name)


        # overwrite yaml file
        with open(self.config_file, "w") as fh:
            yaml.dump(self.global_config, fh)

        # printout successfullly added to global config
        self.menu.add_vertical_margin(20)
        self.menu.add_label("Added offer to saved offers!", align=pygame_menu.locals.ALIGN_CENTER, font_size=30, font_color=(0,200,0))

        # reinitialize all menus
        self.reinitialize_submenus()
        self.reinitialize_main_menu_widgets()

    def reinitialize_submenus(self):
        # reinitialize compare menu
        self.menu._remove_submenu(self.compare_offers_menu)
        del self.compare_offers_menu
        self.compare_offers_menu = CompareMenu("Compare Offers", self.global_config, self.config_file)

        # reinitialize remove menu
        self.menu._remove_submenu(self.remove_offers_menu)
        del self.remove_offers_menu
        self.remove_offers_menu = RemoveMenu("Remove Offers", self.global_config, self.config_file, self.main_menu_object)


    def reinitialize_main_menu_widgets(self):
        self.menu_name_to_widget = {}
        self.main_menu_object.menu.clear()
        self.main_menu_object.create_submenus()
        self.main_menu_object.add_parameter_buttons_and_fields()
        self.main_menu_object.add_navigation_buttons()


class CompareMenu:

    def __init__(self, name, global_config, config_file):

        self.num_saved_offers = len(global_config["initial"]["incomes"])
        self.all_offers = list(global_config["initial"]["incomes"].keys())

        self.name_to_widget = {}
        self.num_rows_per_colum = self.num_saved_offers + 2

        self.config_file = config_file
        self.global_config = global_config
        self.initialize_temporary_config()

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare Offers", columns=2, rows=self.num_rows_per_colum, theme=pygame_menu.themes.THEME_BLUE)
        self.initialize_compare_offers_menu()

    def initialize_temporary_config(self):
        self.temporary_config = copy.deepcopy(self.global_config)
        self.temporary_config["initial"]["incomes"] = {}
        self.temporary_config["simulation_params"]["names_of_parents"] = []


    def add_offer_to_compare_list(self, offer_name):
        # adds an offer to the compare list
        if offer_name not in self.name_to_widget.keys():
            self.menu.add_button(offer_name, partial(self.remove_offer_from_compare_list, offer_name), align=pygame_menu.locals.ALIGN_RIGHT, 
            font_size=20, font_color=(0,0,0),
            )
            self.name_to_widget[offer_name] = self.menu.get_widgets()[-1]

            self.temporary_config["initial"]["incomes"][offer_name] = copy.deepcopy(self.global_config["initial"]["incomes"][offer_name])
            self.temporary_config["simulation_params"]["names_of_parents"].append(offer_name)

    def remove_offer_from_compare_list(self, offer_name):
        # removes an offer from the compare list
        self.menu.remove_widget(self.name_to_widget[offer_name])
        self.name_to_widget.pop(offer_name)
        self.temporary_config["initial"]["incomes"].pop(offer_name)

        self.temporary_config["simulation_params"]["names_of_parents"] = []
        for offer_name in self.temporary_config["initial"]["incomes"].keys():
            self.temporary_config["simulation_params"]["names_of_parents"].append(offer_name)



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

        dirname = os.path.dirname(self.config_file)
        temp_config_file = str(Path(dirname, "temp.yaml"))

        # save config
        with open(temp_config_file, "w") as fh:
            yaml.dump(self.temporary_config, fh)

        # config_path = "configs\job_only_config.yaml"
        financial_simulator = FinancialSimulator(temp_config_file)
        financial_simulator.run_simulation()
        financial_simulator.plot_portfolio("net_worth")

        print(f"do comparison")



class RemoveMenu:

    def __init__(self, name, global_config, config_file, main_menu_object):

        self.name_to_widget = {}
        self.global_config = global_config
        self.config_file = config_file
        self.main_menu_object = main_menu_object
        self.initialize_remove_offers_menu()

    def initialize_temporary_config(self):
        self.temporary_config = copy.deepcopy(self.global_config)
        self.temporary_config["initial"]["incomes"] = {}


    def add_offer_to_remove_list(self, offer_name):
        # adds an offer to the remove list
        if offer_name not in self.name_to_widget.keys():
            self.menu.add_button(offer_name, partial(self.remove_offer_from_remove_list, offer_name), align=pygame_menu.locals.ALIGN_RIGHT, 
            font_size=20, font_color=(0,0,0),
            )
            self.name_to_widget[offer_name] = self.menu.get_widgets()[-1]

            # add the details of the config we selected to a temporary config we will run
            self.temporary_config["initial"]["incomes"][offer_name] = copy.deepcopy(self.global_config["initial"]["incomes"][offer_name])
            

    def remove_offer_from_remove_list(self, offer_name):
        # removes an offer from the compare list
        self.menu.remove_widget(self.name_to_widget[offer_name])
        self.name_to_widget.pop(offer_name)
        self.temporary_config["initial"]["incomes"].pop(offer_name)


    def initialize_remove_offers_menu(self):

        # load global config
        with open(self.config_file, "r") as fh:
            self.global_config = yaml.load(fh, yaml.FullLoader)

        # initialize num_saved offers
        self.num_saved_offers = len(self.global_config["initial"]["incomes"])
        self.all_offers = list(self.global_config["initial"]["incomes"].keys())
        self.num_rows_per_colum = self.num_saved_offers + 2

        # initialize temporary config
        self.initialize_temporary_config()

        # initialize 
        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Remove Offers", columns=2, rows=self.num_rows_per_colum, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.clear()
        self.menu.add_label("Add offers to compare", align=pygame_menu.locals.ALIGN_LEFT, font_size=24, font_color=(0,0,0))

        # add all the options to select
        self.menu.add_vertical_margin(10)
        for offer_name in self.all_offers:
            self.menu.add_button(offer_name, partial(self.add_offer_to_remove_list, offer_name), align=pygame_menu.locals.ALIGN_LEFT, font_size=20, font_color=(0,0,0))

        # add the second column
        self.menu.add_button("Remove", self.remove_offers, align=pygame_menu.locals.ALIGN_TOP, font_size=24, 
            font_color=(210,0,0), 
            background_color=(200, 200, 255),
        )
        self.menu.add_vertical_margin(10)


    def remove_offers(self):

        # remove offer from global config
        for offer_name in self.name_to_widget.keys():
            I = [i for i, name in enumerate(self.global_config["simulation_params"]["names_of_parents"]) if name == offer_name][0]
            self.global_config["simulation_params"]["names_of_parents"].pop(I)
            del self.global_config["initial"]["incomes"][offer_name]

        with open(self.config_file, "w") as fh:
            yaml.dump(self.global_config, fh)

        # printout successfullly added to global config
        self.menu.add_vertical_margin(20)
        self.menu.add_label("removed offer from saved offers!", align=pygame_menu.locals.ALIGN_CENTER, font_size=30, font_color=(200, 0,0))


        # update compare menu
        self.initialize_remove_offers_menu()
        self.reinitialize_main_menu_widgets()

    def reinitialize_main_menu_widgets(self):
        self.menu_name_to_widget = {}
        self.main_menu_object.menu.clear()
        self.main_menu_object.create_submenus()
        self.main_menu_object.add_parameter_buttons_and_fields()
        self.main_menu_object.add_navigation_buttons()


class MainMenu:

    def __init__(self, surface, number=1, name=None, theme=pygame_menu.themes.THEME_BLUE, config_file=r"configs\dev_config.yaml"):

        self.menu = pygame_menu.Menu(MENU_SIZE[0], MENU_SIZE[1], "Compare offerings", theme=theme)

        self.config = self.load_config(config_file)
        self.config_file = config_file

        self.create_submenus()
        self.menu_name_to_widget = {}

        # set defaults from the constructor
        self.default_name = name if name is not None else f"bills{number}"

        self.add_parameter_buttons_and_fields()
        self.add_navigation_buttons()

    def load_config(self, config_file):
        with open(config_file, "r") as fh:
            config = yaml.load(fh, yaml.FullLoader)
        return config

    def create_submenus(self):
        self.config = self.load_config(self.config_file)
        self.job_menu = JobMenu("Add Offer", self.config, self.config_file, self)
        self.simulation_settings_menu = SimulationSettingsMenu("Simulation Settings", self.config, self.config_file, self) # for this just use a fixed expense type

    def add_parameter_buttons_and_fields(self):
        # add parameter buttons and fields
        self.menu.add_button("Simulation Settings", self.simulation_settings_menu.menu, font_size=24, font_color=(0,0,0))
        self.menu.add_button("Add Offer", self.job_menu.menu, font_size=24, font_color=(0,0,0))
        self.menu_name_to_widget["Add Offer"] = self.menu.get_widgets()[-1]

        self.menu.add_button("Remove Offer", self.job_menu.remove_offers_menu.menu, font_size=24, font_color=(0,0,0))
        self.menu_name_to_widget["Remove Offer"] = self.menu.get_widgets()[-1]

        self.menu.add_button("Compare Offers", self.job_menu.compare_offers_menu.menu, font_size=24, font_color=(0,0,0)) # #TODO fix so that it doesn't just copy the instantiation but also updates the version of this menu
        self.menu_name_to_widget["Compare Offers"] = self.menu.get_widgets()[-1]


    def add_navigation_buttons(self):
        # add navigation buttons
        self.menu.add_vertical_margin(40)
        self.menu.add_button("Quit", pygame_menu.events.PYGAME_QUIT, font_size=24, font_color=(0,0,0))

            
    def run(self, surface):
        self.menu.mainloop(surface)


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)
    MainMenu(surface, number=1).run(surface)