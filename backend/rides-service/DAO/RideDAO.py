import sys
sys.path.append('../../rides-service')

from enum import Enum
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,func

from Entities import base
from Entities import DriverVehicle
from Entities import Ride
from Entities import RideMetadata

from services import RideService

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///rides_service.db', echo=True)

# Create a base class for declarative class definitions
Base = base.Base
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

session = Session()

class DriverStatus(Enum):
    DRIVING = 0
    WAITING = 2
    OFFLINE = 3

class RideStatus(Enum):
    PENDING = 1     # NO DRIVER HAS ACCEPTED THE RIDE
    ACCEPTED = 2    # DRIVER HAS ACCEPTED THE RIDE
    PASSENGER_PICKED = 3    # PASSENGER HAS BEEN PICKED 
    DRIVER_CANCELLED = 4  # RIDE HAS BEEN CANCELLED BY DRIVER
    PASSENGER_CANCELLED = 5   # RIDE HAS BEEN CANCELLED BY RIDER
    COMPLETED = 6   # RIDE HAS BEEN COMPLETED

class RideDAO :
    
    SAFE_RIDE_RATING = 4
    SAFE_RIDE_NUMRIDES = 3
    @staticmethod
    def create_drivervehicle(driver_id, vehicle_id) : 
        vehicle = RideService.RideService.fetch_vehicles_detail(vehicle_id)
        driver_vehicle = DriverVehicle(driver_id = driver_id, vehicle_id = vehicle_id, driver_status = DriverStatus.OFFLINE, model = vehicle.model, current_location = None)
        session.add(driver_vehicle)
        session.commit()
        return driver_vehicle.driver_id 
    
    @staticmethod
    def get_drivervehicle(driver_id) :
        driver_vehicles = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id).all()
        final_list = []
        for driver_vehicle in driver_vehicles :
            vehicle = RideService.RideService.fetch_vehicles_detail(driver_vehicle.vehicle_id)
            final_list.append({'driver_id' : driver_vehicle.driver_id, 'vehicle_id' : driver_vehicle.vehicle_id, 'model' : vehicle.model,'status':driver_vehicle.driver_status,'current_location':driver_vehicle.current_location})
        return final_list

    @staticmethod
    def fetch_rides_passsenger(source, destination, is_secure) : 
        driver_vehicles = session.query(DriverVehicle).filter(DriverVehicle.driver_status == DriverStatus.WAITING).all()
        if is_secure:
            # Subquery to calculate average rating and count of rides per driver
            subquery = (
                session.query(
                    Ride.driver_id,
                    func.avg(RideMetadata.ride_rating).label("avg_rating"),
                    func.count(Ride.ride_id).label("num_rides")
                )
                .join(RideMetadata, Ride.ride_id == RideMetadata.ride_id)
                .group_by(Ride.driver_id)
                .having(
                    func.avg(RideMetadata.ride_rating) >= RideDAO.SAFE_RIDE_RATING,
                    func.count(Ride.ride_id) >= RideDAO.SAFE_RIDE_NUMRIDES
                )
                .subquery()
            )

            # Fetch DriverVehicle records with the desired conditions
            driver_vehicles = (
                session.query(DriverVehicle)
                .join(subquery, DriverVehicle.driver_id == subquery.c.driver_id)
                .filter(DriverVehicle.driver_status == DriverStatus.WAITING)
                .all()
            )

        final_list = []
        for driver_vehicle in driver_vehicles :
            vehicle = RideService.RideService.fetch_vehicles_detail(driver_vehicle.vehicle_id)
            driver = RideService.RideService.fetch_driver_details(driver_vehicle.driver_id)
            fare  = RideService.RideService.get_fare(source, destination)
            final_list.append({'driver_name':driver.name, 'vehicle_id' : driver_vehicle.vehicle_id, 'model' : vehicle.model,'vehicle_number':vehicle.registration_number,'fare':fare})
        return final_list

    @staticmethod
    def match_ride(passenger_id, source , destination , is_secure , vehicle_model) : 
        '''Match a ride with the given parameters'''
        '''Ride Entity is created here'''
        ride = Ride(ride_id = str(uuid.uuid4()), driver_id = None, passenger_id = passenger_id, start_location = source, drop_location = destination)
        ride_metadata = RideMetadata(id = str(uuid.uuid4()), ride_id = ride.ride_id, ride_otp = str(uuid.uuid4()), ride_status = 1, ride_rating = None, vehicle_id = None, vehicle_model = vehicle_model ,is_secure = False)
        session.add(ride)
        session.add(ride_metadata)
        session.commit()
        return ride.ride_id

    @staticmethod
    def fetch_rides_driver(source , destination) : 
        '''Fetch rides for a driver'''
        '''Just fetch all the rides where status is pending'''
        return session.query(Ride).filter(Ride.status == RideStatus.PENDING).all()

    @staticmethod
    def accept_ride_driver(ride_id) :
        '''accept the ride for a driver'''
        '''set the status of the ride to accepted'''
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        ride.status = RideStatus.ACCEPTED
        session.commit()
        return ride.ride_id
    
    @staticmethod
    def pickup_passenger(ride_id, otp) : 
        '''change the status of the ride to start'''
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        #match otp
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        if ride_metadata.ride_otp != otp : 
            return None
        ride.status = RideStatus.PASSENGER_PICKED
        session.commit()
        return ride.ride_id
    
    @staticmethod
    def complete_ride(ride_id) : 
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        ride.status = RideStatus.COMPLETED
        session.commit()
        #on completing the ride, change drivervehicle status to WAITING
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == ride.driver_id).first()
        driver_vehicle.driver_status = 2
        session.commit()
        return ride.ride_id 
    
    @staticmethod
    def change_status(driver_id, status) : 
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id).first()
        #driver status can't be changed manually if he is driving 
        if driver_vehicle.driver_status == DriverVehicle.DRIVING : 
            return None
        driver_vehicle.driver_status = status
        session.commit()
        return driver_vehicle.driver_id 
    
    @staticmethod
    def get_ride_fare(ride_id):
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        fare = RideService.RideService.get_fare(ride.start_location,ride.drop_location,ride_metadata.vehicle_model)
        return fare

    
    '''Write methods for car pooling'''