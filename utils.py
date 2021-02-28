import numpy as np
import matplotlib.pyplot as plt


VALID_LOCATIONS = ["israel", "providence", "nyc"]
MONTHLY_INCOME_WITH_BONUSES = "base_salary_with_bonuses"
JOB_RELATED_PORTFOLIOS = ["keren_hishtalmut", "pension", "company_stock", "options"]
NAME_OF_MAIN_PORTFOLION = "main_portfolio"
NAMES_OF_PARENTS = ["benjy", "inbar"]



class PortFolioTracker:

    def __init__(self, portfolios):
        self.portflio_trackers = {}
        self.parent_name = []
        for parent_name in portfolios.keys():
            self.parent_names.append(parent_name)
            self.portflio_trackers[parent_name] = {}
            for portfolio_name, portfolio_balance in portfolios[parent_name].items():
                self.portflio_trackers[parent_name][portfolio_name] = [portfolio_balance]

    def add_new_values_of_portfolios(self, portfolios):
        for parent_name in portfolios.keys():
            for portfolio_name, portfolio_balance in portfolios[parent_name].items():
                self.portflio_trackers[parent_name][portfolio_name].append(portfolio_balance)


    def get_portfolios_trackers(self):
        return self.portflio_trackers


    def get_net_worth(self, parent_name):
        net_worth = None
        for name in self.portflio_trackers[parent_name].keys():
            portfolio_balance = self.portflio_trackers[parent_name][name]
            if net_worth is None:
                net_worth = portfolio_balance
            else:
                net_worth = [i + j for i, j in zip(net_worth, portfolio_balance)] # combine all values
        return net_worth

        
    def get_portfolio_balance(self, parent_name, portfolio_name):
            if portfolio_name == "net_worth":
                return self.get_net_worth(parent_name)
            else:
                return self.portflio_trackers[parent_name][portfolio_name]

        
    def plot_portfolio(self, total_num_months, portfolio_name, target_net_worth_for_retirement=3000):
        years = np.linspace(0, total_num_months/12, total_num_months)
        retirment_target = target_net_worth_for_retirement * np.ones(total_num_months)

        for parent_name in NAMES_OF_PARENTS:
            # if portfolio_name == "net_worth":
            #     portfolio_balance = self.get_net_worth(parent_name)
            # else:
            #     portfolio_balance = self.portflio_trackers[parent_name][portfolio_name]

            portfolio_balance = self.get_portfolio_balance(parent_name, portfolio_name)
            plt.plot(years, portfolio_balance)

        plt.plot(years, retirment_target, "--k")
        plt.legend(NAMES_OF_PARENTS + ["target net worth for retirement"])
        plt.xlabel("years")
        plt.ylabel("balance (thousands of shekels)")
        plt.title(f"{portfolio_name} balance throughout the years")
        plt.show()


    def plot_portfolio_(self, portfolio_balances, portfolio_name, target_net_worth_for_retirement=3000):

        total_num_months = len()
        years = np.linspace(0, total_num_months/12, total_num_months)
        retirment_target = target_net_worth_for_retirement * np.ones(total_num_months)

        for parent_name in portfolio_balances.keys():
            # if portfolio_name == "net_worth":
            #     portfolio_balance = self.get_net_worth(parent_name)
            # else:
            #     portfolio_balance = self.portflio_trackers[parent_name][portfolio_name]

            # portfolio_balance = self.get_portfolio_balance(parent_name, portfolio_name)


            portfolio_balance = portfolio_balances[parent_name]["expected_balance"] # assuming all the arrays are the same length and None values have been handled
            balance_error = portfolio_balances[parent_name]["error"] 
            plt.errorbar(years, portfolio_balance, yerr=balance_error)

        plt.plot(years, retirment_target, "--k")
        plt.legend(NAMES_OF_PARENTS + ["target net worth for retirement"])
        plt.xlabel("years")
        plt.ylabel("balance (thousands of shekels)")
        plt.title(f"{portfolio_name} balance throughout the years")
        plt.show()


    def plot_all_portfolios(self, total_num_months, target_net_worth_for_retirement=3000):
        years = np.linspace(0, total_num_months/12, total_num_months)
        retirment_target = target_net_worth_for_retirement * np.ones(total_num_months)


        portfolio_names = ["net_worth"] + list(self.portflio_trackers[NAMES_OF_PARENTS[0]].keys())
        fig, all_ax = plt.subplots(len(portfolio_names), figsize=(20,10))
        i = 0

        for ax, portfolio_name in zip(all_ax, portfolio_names):
                
            for parent_name in NAMES_OF_PARENTS:
                # if portfolio_name == "net_worth":
                #     portfolio_balance = self.get_net_worth(parent_name)
                # else:
                #     portfolio_balance = self.portflio_trackers[parent_name][portfolio_name]

                # if portfolio_name == "net_worth":
                #     portfolio_balance = self.get_net_worth(parent_name)
                # else:
                #     portfolio_balance = self.portflio_trackers[parent_name][portfolio_name]

                portfolio_balance = self.get_portfolio_balance(parent_name, portfolio_name)
                plt.plot(years, portfolio_balance)

                portfolio_balance = self.get_portfolio_balance(parent_name, portfolio_name)
                ax.plot(years, portfolio_balance)

            ax.plot(years, retirment_target, "--k")
            ax.legend(NAMES_OF_PARENTS + ["target net worth for retirement"])
            ax.set_title(f"{portfolio_name} balance")
            ax.yaxis.set_ticks(np.arange(0, 1.2 * max(np.max(portfolio_balance), np.max(portfolio_balance)), 1000))
            ax.grid()

            if i < (len(all_ax) - 1):
                ax.xaxis.set_ticklabels([])
            i += 1


        plt.xlabel("years")
        plt.ylabel("balance (thousands of shekels)")
        plt.show()


class MultiRunTracker:

    def __init__(self, number_of_repetitions):
        self.number_of_repetitions = number_of_repetitions
        self.trackers = [None for _ in range(number_of_repetitions)]

    def add_new_values_of_portfolios(self, portfolios, current_repetition):
        if self.trackers[current_repetition] is None:
            self.trackers[current_repetition] = PortFolioTracker(portfolios)
            self.parent_names = self.trackers[current_repetition].parent_names
        else:
            self.trackers[current_repetition].add_new_values_of_portfolios(portfolios)

    def plot_portfolio(self, portfolio_name, goal=3000):

        portfolio_balances = {}
        for parent_name in self.parent_names:
            # initialize array
            portfolio_balances[parent_name] = {}
            balance_array = []

            # parse palances
            for current_repetition in range(self.number_of_repetitions):
                balance = self.trackers[current_repetition].get_portfolio_balance(parent_name, portfolio_name)
                balance_array.append(balance)

            # fix missing values
            portfolio_balances[parent_name]["expected_balance"] = np.mean(balance_array, 0)
            portfolio_balances[parent_name]["error"] = np.std(balance_array, 0)


a = [[1,2,3,4,5], [2,4,6]]