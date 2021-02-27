import copy
from utils import *


class Expense:
    def __init__(self):
        self.age = 0

    def increment_by_one_year(self):
        self.age += 1

    def get_expense(self): # in thousands of shekels, per month
        raise NotImplementedError

class TotalExpenses:
    def __init__(self, dict_of_expenses):
        self.dict_of_expenses = dict_of_expenses
        self.num_kids = 0

    def add_expense(self, expense_name, expense):
        self.dict_of_expenses[expense_name] = expense

    def remove_expense(self, expense_name):
        del self.dict_of_expenses[expense_name]

    def increment_by_one_year(self):
        for expense_name in self.dict_of_expenses.keys():
            self.dict_of_expenses[expense_name].increment_by_one_year()

    def get_monthly_expenses(self):
        total_expenses = 0
        for expense_name in self.dict_of_expenses.keys():
            total_expenses += self.dict_of_expenses[expense_name].get_expense()
        return total_expenses

    def have_kid(self, location, num_after_school_activities=2):
        expense_name = "kid" + str(self.num_kids)
        self.dict_of_expenses[expense_name] = Kid(location, num_after_school_activities)
        self.update_num_kids()

    def update_num_kids(self):
        self.num_kids += 1
        for expense_name in self.dict_of_expenses.keys():
            if hasattr(self.dict_of_expenses[expense_name], "num_kids"):
                self.dict_of_expenses[expense_name].num_kids += 1

    def update_location(self, new_location):
        if new_location not in VALID_LOCATIONS:
            raise ValueError(f"recieved unsupported location {new_location}, allowed locations are: {VALID_LOCATIONS}")

        for expense_name in self.dict_of_expenses.keys():
            if hasattr(self.dict_of_expenses[expense_name], "location"):
                self.dict_of_expenses[expense_name].location = new_location


class Kid(Expense):
    def __init__(self, location="israel", num_after_school_activities=2):
        super().__init__() 
        self.location = location
        self.num_after_school_activities = num_after_school_activities

    def get_expenses_ages_0_to_4(self):
        if (self.location == "israel") or (self.location == "providence"):
            daycare = 3
            food = 0.3 if self.age <= 1 else 0.5
            clothes = 0.3 if self.age <= 2 else 0.5
            diapers = 0.3 if self.age <= 3 else 0
        elif self.location == "nyc":
            daycare = 6
            food = 0.3 if self.age <= 1 else 0.5
            clothes = 0.3 if self.age <= 2 else 0.5
            diapers = 0.3 if self.age <= 3 else 0
        else:
            raise ValueError("unsupported location")

        return daycare + food + clothes + diapers

    def get_expenses_ages_4_to_14(self):
        school = 1
        school_supplies = 0.2
        food = 1 if self.age <= 10 else 1.5
        clothes = 0.3 if self.age <= 10 else 0.5
        activities = 0.3 * self.num_after_school_activities
        allowance = 0.2
        total = school + school_supplies + food + clothes + activities + allowance
        return total

    def get_expenses_ages_14_to_18(self):
        school = 1
        school_supplies = 0.4
        food = 2
        clothes = 0.6
        activities = 0.3 * self.num_after_school_activities
        allowance = 0.5
        total = school + school_supplies + food + clothes + activities + allowance
        return total

    def get_expenses_ages_18_to_21(self):
        food = 1
        clothes = 0.2
        allowance = 1
        total = food + clothes + allowance
        return total

    def get_expenses_ages_21_to_23(self):
        food = 2
        allowance = 1
        total = food + allowance
        return total

    def get_expenses_ages_23_27(self):
        allowance = 2
        return allowance

    def get_expense(self):
        if self.age <= 4:
            return self.get_expenses_ages_0_to_4()

        elif 4 < self.age <= 14:
            return self.get_expenses_ages_4_to_14()

        elif 14 < self.age <= 18:
            return self.get_expenses_ages_14_to_18()

        elif 18 < self.age <= 21:
            return self.get_expenses_ages_18_to_21()

        elif 21 < self.age <= 23:
            return self.get_expenses_ages_21_to_23()

        elif 23 < self.age <= 27:
            return self.get_expenses_ages_23_27()
        
        else:
            return 0



class House(Expense):
    def __init__(self, full_price, down_payment, monthly_payment):
        super().__init__()
        self.full_price = full_price
        self.down_payment = down_payment
        self.monthly_payment = monthly_payment

        self.payed_down_payment = False
        self.remaining_price = copy.deepcopy(full_price)

    def get_expense(self):  # add maintanance expenses and furnature expense
        if self.payed_down_payment:
            if (self.remaining_price > 0):
                self.remaining_price = (self.remaining_price - self.monthly_payment)
                return self.monthly_payment
            else:
                return 0
        else:
            self.remaining_price = self.remaining_price - self.down_payment
            self.payed_down_payment = True
            return self.down_payment


class MBA(Expense):
    def __init__(self, down_payment=100):
        super().__init__() 
        self.down_payment = down_payment
        self.payed_down_payment = False

    def get_expense(self):
        if self.payed_down_payment:
            return 0
        else:
            self.payed_down_payment = True
            return self.down_payment


class FixedPriceApartment(Expense):
    def __init__(self, monthly_payment):
        super().__init__() 
        self.monthly_payment = monthly_payment

    def get_expense(self):
        return self.monthly_payment


class LocationDependentApartment(Expense):
    def __init__(self, location, num_kids):
        super().__init__() 
        self.location = location
        self.num_kids = num_kids

    def get_apartment_price_in_israel_per_number_of_kids(self):
        if self.num_kids <= 1:
            return 6
        elif 1 < self.num_kids <= 2:
            return 8
        elif 2 < self.num_kids:
            return 9

    def get_apartment_price(self):
        if (self.location == "israel") or (self.location == "providence"):
            price = self.get_apartment_price_in_israel_per_number_of_kids()
        elif (self.location == "nyc"):
            price_in_israel_or_pvd = self.get_apartment_price_in_israel_per_number_of_kids()
            price = price_in_israel_or_pvd + 3
        else:
            raise ValueError("invalid location")
        return price

    def get_expense(self):
        return self.get_apartment_price()


class Bills(Expense):
    def __init__(self, **kwargs):
        super().__init__() 

    def get_expense(self):
        electricity = 0.8
        gas = 0.2
        arnona = 0.4
        water = 0.3
        total = electricity + gas + arnona + water
        return total


class Fun(Expense):
    def __init__(self, location="israel", **kwargs):
        super().__init__()
        self.location = location

    def get_expense(self):
        if self.age <= 2:
            if (self.location == "israel") or (self.location == "providence"):
                return 4
            elif self.location == "usa":
                return 6
        else:
            return 2

class Pet(Expense):
    def __init__(self, **kwargs):
        super().__init__() 

    def get_expense(self):
        food = 0.2
        ensaurance = 0.1
        vet = 0.1
        total = food + ensaurance + vet
        return total


class LivingExpenses(Expense):
    def __init__(self, **kwargs):
        super().__init__() 

    def get_expense(self):
        food = 2
        other_costs = 2
        total = food + other_costs
        return total


class Car(Expense):
    def __init__(self, average_car_price=80, payed_down_payment=False, starting_age_of_initial_car=5, average_car_lifetime=7):
        super().__init__()
        self.payed_down_payment = payed_down_payment
        self.average_car_price = average_car_price
        self.average_car_lifetime = average_car_lifetime
        self.age = starting_age_of_initial_car

    def increment_by_one_year(self):
        super().increment_by_one_year()
        if self.age % self.average_car_lifetime == 0:
            self.payed_down_payment = False

    def get_down_payment_price(self):
        if self.payed_down_payment:
            return 0
        else:
            self.payed_down_payment = True
            return self.average_car_price
         
    def get_expense(self):
        down_payment = self.get_down_payment_price()
        gas = 1
        repairs = 0.5 # make these probabalistic and with higher amounts
        license = 0.2
        insaurance = 0.3
        total = down_payment + gas + repairs + license + insaurance
        return total





class FamilyTrip(Expense):
    def __init__(self, num_days, num_kids, cost_per_day_per_person=0.6, flights_per_person=3):
        super().__init__()
        self.num_days = num_days
        self.num_kids = num_kids
        self.cost_per_day_per_person = cost_per_day_per_person
        self.flights_per_person = flights_per_person
        self.went_on_trip = False

    def increment_by_one_year(self):
        super().increment_by_one_year()
        self.went_on_trip = False
        
    def get_expense(self):
        if self.went_on_trip:
            return 0

        self.went_on_trip = True
        total_num_people = (self.num_kids + 2)
        total_cost_per_day = self.cost_per_day_per_person * total_num_people
        total_flights_cost = self.flights_per_person * total_num_people
        total_trip_cost = total_cost_per_day * self.num_days
        total = total_trip_cost + total_flights_cost
        return total


class BigFamilyTrip(FamilyTrip):
    def __init__(self, num_days, num_kids, cost_per_day_per_person=0.6, flights_per_person=3):
        super().__init__(num_days, num_kids, cost_per_day_per_person, flights_per_person)

class SmallFamilyTrip(FamilyTrip):
    def __init__(self, num_days, num_kids, cost_per_day_per_person=0.4, flights_per_person=1):
        super().__init__(num_days, num_kids, cost_per_day_per_person, flights_per_person)

class WeekendTrips(FamilyTrip):
    def __init__(self, num_kids, num_days, cost_per_day_per_person=0.4, flights_per_person=0):
        super().__init__(num_days, num_kids, cost_per_day_per_person, flights_per_person)
