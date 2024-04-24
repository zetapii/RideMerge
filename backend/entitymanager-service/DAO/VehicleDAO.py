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
engine = create_engine('sqlite:///entity_service.db', echo=True)

# Create a base class for declarative class definitions
Base = base.Base
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

session = Session()

Driver = Driver.Driver
Passenger = Passenger.Passenger
Vehicle = Vehicle.Vehicle 

class VehicleDAO : 

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
    def get_vehicle(id):
        vehicles = session.query(Vehicle).filter(Vehicle.id == id).first()
        return vehicles 
        
    @staticmethod
    def get_vehicles():
        vehicle = session.query(Vehicle).all()
        return vehicle