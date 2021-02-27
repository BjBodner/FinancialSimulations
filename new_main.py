from financial_simulator import FinancialSimulator


if __name__ == "__main__":

    config_path = "configs/starting_point.yaml"
    financial_simulator = FinancialSimulator(config_path)
    financial_simulator.run_simulation()
    financial_simulator.plot_all_portfolios()