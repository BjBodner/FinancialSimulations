from financial_simulator import FinancialSimulator


if __name__ == "__main__":

    # config_path = "configs/config.yaml"
    config_path = "configs\job_only_config.yaml"
    financial_simulator = FinancialSimulator(config_path)
    financial_simulator.run_simulation()
    # financial_simulator.plot_all_portfolios()
    financial_simulator.plot_portfolio("net_worth")