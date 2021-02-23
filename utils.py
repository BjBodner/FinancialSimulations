VALID_LOCATIONS = ["israel", "providence", "nyc"]
MONTHLY_INCOME_WITH_BONUSES = "base_salary_with_bonuses"
JOB_RELATED_PORTFOLIOS = ["keren_hishtalmut", "pension", "company_stock", "options"]
NAME_OF_MAIN_PORTFOLION = "main_portfolio"



class PortFolioTracker:

    def __init__(self, portfolios):
        self.portflio_trackers = {}
        for parent_name in portfolios.keys():
            self.portflio_trackers[parent_name] = {}
            for portfolio_name, portfolio_balance in portfolios[parent_name].items():
                self.portflio_trackers[parent_name][portfolio_name] = [portfolio_balance]

    def add_new_values_of_portfolios(self, portfolios):
        for parent_name in portfolios.keys():
            for portfolio_name, portfolio_balance in portfolios[parent_name].items():
                self.portflio_trackers[parent_name][portfolio_name].append(portfolio_balance)

    def get_portfolios_trackers(self):
        return self.portflio_trackers
