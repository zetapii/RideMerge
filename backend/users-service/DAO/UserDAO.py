from Entities import User, Passenger, Driver

class UserDAO:
    def __init__(self):
        passenger_list = []
        driver_list = []
        vehicle_list = []

    def add_passenger(self, passenger):
        self.passenger_list.append(passenger)

    def add_driver(self, driver):
        self.driver_list.append(driver)

    def add_vehicle(self, vehicle):
        self.vehicle_list.append(vehicle)

    '''TODO -> Other CRUD operations for User, Passenger, Driver, Vehicle'''