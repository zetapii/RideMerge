import sys
sys.path.append('../../entitymanager-service')

from enum import Enum
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from Entities import base
from Entities import Driver
from Entities import Passenger
from Entities import Vehicle

from services import EntityService

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///users_service.db', echo=True)

# Create a base class for declarative class definitions
Base = base.Base
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

session = Session()

Driver = Driver.Driver
Passenger = Passenger.Passenger
Vehicle = Vehicle.Vehicle 

class EntityDAO : 

    #write method to create driver adn create passenger
    @staticmethod
    def create_driver(name, password, email, phone, driving_license):
        '''Create a driver'''
        '''check if same phone number exists or not'''
        driver = session.query(Driver).filter(Driver.phone == phone).first()
        if driver:
            return None
        driver = Driver(id = str(uuid.uuid4()), name = name, password = password, email = email, phone = phone, driving_license = driving_license)
        session.add(driver)
        session.commit()
        return driver.id

    @staticmethod
    def create_passenger(name, password, email, phone):
        '''Create a passenger'''
        '''check if same phone number exists or not'''
        passenger = session.query(Passenger).filter(Passenger.phone == phone).first()
        if passenger : 
            return None
        passenger = Passenger(id = str(uuid.uuid4()), name = name, password = password, email = email, phone = phone)
        session.add(passenger)
        session.commit()
        return passenger.id    
    
    @staticmethod
    def add_vehicle(driver_id , vehicle_model , registration_number , insurance_number , manufacturer , manufacturing_year):
        '''Add a vehicle for a driver but first checking if vehicle with same registration number doesn't already exits'''
        vehicle = session.query(Vehicle).filter(Vehicle.registration_number == registration_number).first()
        if vehicle:
            return None
        driver = session.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            return None
        vehicle = Vehicle(id = str(uuid.uuid4()), driver_id = driver_id , vehicle_model = vehicle_model, registration_number = registration_number, insurance_number = insurance_number, manufacturer = manufacturer, manufacturing_year = manufacturing_year)
        session.add(vehicle)
        session.commit()

        EntityService.EntityService.create_driver_vehicle(driver_id, vehicle.id)

        return vehicle.id 
    
    @staticmethod
    def login_passenger(phone, password):
        '''Login a passenger'''
        passenger = session.query(Passenger).filter(Passenger.phone == phone, Passenger.password == password).first()
        if passenger:
            return passenger.id
        return None
    
    @staticmethod
    def login_driver(phone, password):
        '''Login a driver'''
        driver = session.query(Driver).filter(Driver.phone == phone, Driver.password == password).first()
        if driver:
            return driver.id
        return None

    @staticmethod
    def get_driver(id):
        driver = session.query(Driver).filter(Driver.id == id).first()
        return driver
    
    @staticmethod
    def get_drivers():
        drivers = session.query(Driver).all()
        return drivers

    @staticmethod
    def get_passenger(id):
        passenger = session.query(Passenger).filter(Passenger.id == id).first()
        return passenger
    
    @staticmethod
    def get_passengers():
        passengers = session.query(Passenger).all()
        return passengers
    
    @staticmethod
    def get_vehicle(id):
        vehicles = session.query(Vehicle).filter(Vehicle.id == id).first()
        return vehicles 
        
    @staticmethod
    def get_vehicles():
        vehicle = session.query(Vehicle).all()
        return vehicle