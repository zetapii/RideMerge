import sys
sys.path.append('../../rides-service')

from enum import Enum
from enum import IntEnum

import uuid
import time
from datetime import datetime
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

DriverVehicle = DriverVehicle.DriverVehicle
Ride = Ride.Ride
RideMetadata = RideMetadata.RideMetadata

class DriverStatus(IntEnum):
    DRIVING = 0
    WAITING = 1
    OFFLINE = 2

class RideStatus(IntEnum):
    PENDING = 1     # NO DRIVER HAS ACCEPTED THE RIDE
    ACCEPTED = 2    # DRIVER HAS ACCEPTED THE RIDE
    PASSENGER_PICKED = 3    # PASSENGER HAS BEEN PICKED 
    DRIVER_CANCELLED = 4  # RIDE HAS BEEN CANCELLED BY DRIVER
    PASSENGER_CANCELLED = 5   # RIDE HAS BEEN CANCELLED BY RIDER
    COMPLETED = 6   # RIDE HAS BEEN COMPLETED

class RideDAO :
    
    SAFE_RIDE_RATING = 0
    SAFE_RIDE_NUMRIDES = 0

    @staticmethod
    def create_drivervehicle(driver_id, vehicle_id) :
        vehicle = RideService.RideService.fetch_vehicles_detail(vehicle_id)
        if session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id, DriverVehicle.vehicle_id == vehicle_id).first() :
            return None
        driver_vehicle = DriverVehicle(id = str(uuid.uuid4()) ,driver_id = driver_id, vehicle_id = vehicle_id, driver_status = 2, current_location = None,model = vehicle['vehicle_model'])
        session.add(driver_vehicle)
        session.commit()
        return driver_vehicle.driver_id 
    
    @staticmethod
    def get_drivervehicle(driver_id) :
        driver_vehicles = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id).all()
        final_list = []
        for driver_vehicle in driver_vehicles :
            vehicle = RideService.RideService.fetch_vehicles_detail(driver_vehicle.vehicle_id)
            final_list.append({'id': driver_vehicle.id, 'driver_id' : driver_vehicle.driver_id, 'vehicle_id' : driver_vehicle.vehicle_id, 'model' : vehicle['vehicle_model'],'status':DriverStatus(driver_vehicle.driver_status).name,'current_location':driver_vehicle.current_location,'registration_number':vehicle['registration_number']})
        print("wer are pringint the final list")
        return final_list

    @staticmethod
    def fetch_rides_passsenger(source, destination, is_secure, passenger_id) : 
        driver_vehicles = session.query(DriverVehicle).filter(DriverVehicle.driver_status == 1).all()
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
        ##initialise a set and then maybe convert back to list
        for driver_vehicle in driver_vehicles :
            vehicle = RideService.RideService.fetch_vehicles_detail(driver_vehicle.vehicle_id)
            driver = RideService.RideService.fetch_driver_details(driver_vehicle.driver_id)
            fare  = RideService.RideService.get_fare(source, destination, vehicle['vehicle_model'],passenger_id)
            final_list.append({'driver_name':driver['name'], 'vehicle_id' : driver_vehicle.vehicle_id, 'model' : vehicle['vehicle_model'],'vehicle_number':vehicle['registration_number'],'fare':fare})
        return final_list

    @staticmethod
    def book_ride(passenger_id, source , destination , is_secure , vehicle_model , is_latlan) : 
        '''Match a ride with the given parameters'''
        '''Ride Entity is created here'''
        current_ride = RideDAO.get_current_ride_passenger(passenger_id)
        if current_ride :
            return None
        passenger = RideService.RideService.fetch_passenger_details(passenger_id)
        distance,duration = None , None
        if is_latlan and is_latlan == True : 
            distance,duration = RideService.RideService.fetch_distance_details(source,destination)
        ride = Ride(ride_id = str(uuid.uuid4()), passenger_id = passenger_id, start_location = source, drop_location = destination)
        fare = RideService.RideService.get_fare(source, destination, vehicle_model,passenger_id)
        ride_metadata = RideMetadata(id = str(uuid.uuid4()), ride_id = ride.ride_id, ride_status = 1, vehicle_model = vehicle_model ,is_secure = is_secure, passenger_name = passenger.get('name'),ride_fare = fare)
        if distance : 
            ride_metadata.ride_distance = distance
        if duration :
            ETR_timestamp = duration + int(time.time())
            ETR_timestamp += 19800
            ETR_readable = datetime.utcfromtimestamp(ETR_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            ride_metadata.ride_ETR = ETR_readable
        session.add(ride)
        session.add(ride_metadata)
        session.commit()
        print("this is ride ",ride)
        return ride.ride_id
    
    @staticmethod
    def fetch_rides_driver(driver_id) :
        print("we got here")
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id,DriverVehicle.driver_status==int(DriverStatus.WAITING)).first()
        print("this is driver_vehicle which maybe empty", driver_vehicle)
        if not driver_vehicle:
            return None
        '''
        driver_rating = session.query(func.avg(RideMetadata.ride_rating)).join(RideMetadata, RideMetadata.ride_id == Ride.ride_id).filter(Ride.driver_id == driver_id).first()
        cnt_rides = session.query(func.count(Ride.ride_id)).filter(Ride.driver_id == driver_id).first()
        '''
        # Join Ride with RideMetadata and filter by driver_id for average rating
        driver_rating = session.query(func.avg(RideMetadata.ride_rating)) \
                            .join(Ride, Ride.ride_id == RideMetadata.ride_id) \
                            .filter(Ride.driver_id == driver_id) \
                            .first()

        # Count rides for the driver
        cnt_rides = session.query(func.count(Ride.ride_id)) \
                        .filter(Ride.driver_id == driver_id) \
                        .first()
        driver_rating = driver_rating[0]
        cnt_rides = cnt_rides[0]
        if not driver_rating: 
            driver_rating=0
        if driver_rating < RideDAO.SAFE_RIDE_RATING or cnt_rides < RideDAO.SAFE_RIDE_NUMRIDES:
            return session.query(Ride).join(RideMetadata, Ride.ride_id == RideMetadata.ride_id).filter(RideMetadata.ride_status == RideStatus.PENDING, RideMetadata.is_secure == False, RideMetadata.vehicle_model == driver_vehicle.model).all()
        else : 
            return session.query(Ride).join(RideMetadata, Ride.ride_id == RideMetadata.ride_id).filter(RideMetadata.ride_status == int(RideStatus.PENDING) , RideMetadata.vehicle_model == driver_vehicle.model).all()

    @staticmethod
    def accept_ride_driver(ride_id,driver_id) :
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id,DriverVehicle.driver_status==int(DriverStatus.WAITING)).first()
        if not driver_vehicle:
            return None
        print(ride_id)
        print(driver_id)
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        ride.driver_id = driver_id
        session.commit()
        
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        if ride_metadata.ride_status != int(RideStatus.PENDING) :
            return None
        ride_metadata.ride_status = int(RideStatus.ACCEPTED)
        ride_metadata.vehicle_id = driver_vehicle.vehicle_id
        ride_metadata.ride_otp = str(uuid.uuid4())

        driver = RideService.RideService.fetch_driver_details(driver_id)
        ride_metadata.driver_name = driver.get('name')

        session.commit()

        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == driver_id).first()
        driver_vehicle.driver_status = int(DriverStatus.DRIVING)
        session.commit()

        return ride.ride_id
    
    @staticmethod
    def pickup_passenger(ride_id, otp) : 
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        if not ride : 
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        print(ride_metadata.ride_status)
        if ride_metadata.ride_status != int(RideStatus.ACCEPTED) :
            return None
        if ride_metadata.ride_otp != otp : 
            return None
        ride_metadata.ride_status = int(RideStatus.PASSENGER_PICKED)
        print(ride_metadata.ride_status)
        session.commit()
        return ride.ride_id
    
    @staticmethod
    def complete_ride(ride_id) : 
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        if (not ride_metadata) or int(RideStatus.PASSENGER_PICKED):
            return None
        ride_metadata.ride_status = int(RideStatus.COMPLETED)
        session.commit()
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == ride.driver_id).first()
        driver_vehicle.driver_status = DriverStatus.WAITING
        session.commit()
        return ride_metadata.ride_id
    
    @staticmethod
    def change_status(driver_vehicle_id,status) :
        ##driving status status can't be manually changed to waiting 
        if status not in [1,2] :
            return None
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.id == driver_vehicle_id).first()
        #driving status status can't be changed manually driver is driving 
        if (not driver_vehicle) or (driver_vehicle.driver_status == DriverStatus.DRIVING) : 
            return None
        driver_vehicle.driver_status = status
        session.commit()
        return driver_vehicle.driver_id 
    
    @staticmethod
    def get_ride_fare(ride_id):
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        if not ride : 
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        fare = RideService.RideService.get_fare(ride.start_location,ride.drop_location,ride_metadata.vehicle_model)
        return fare
    
    @staticmethod
    def get_ride_details(ride_id):
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        if not ride : 
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        return {
                'driver_name' : ride_metadata.driver_name,
                'passenger_name' : ride_metadata.passenger_name,
                'ride_id': ride.ride_id,
                'driver_id': ride.driver_id,
                'passenger_id': ride.passenger_id,
                'start_location': ride.start_location,
                'drop_location': ride.drop_location,
                'status': RideStatus(ride_metadata.ride_status).name,
                'vehicle_id': ride_metadata.vehicle_id,
                'vehicle_model': ride_metadata.vehicle_model,
                'ride_otp': ride_metadata.ride_otp,
                'is_secure': ride_metadata.is_secure,
                'fare': ride_metadata.ride_fare,
                'distance': ride_metadata.ride_distance,
                'ETR': ride_metadata.ride_ETR}
    
    @staticmethod
    def get_current_ride_driver(driver_id):
        query = session.query(Ride).join(RideMetadata, Ride.ride_id == RideMetadata.ride_id)        
        ride = query.filter(Ride.driver_id == driver_id, 
                            RideMetadata.ride_status.notin_([4, 5, 6])).first()
        if not ride:
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride.ride_id).first()
        return {'passenger_name': ride_metadata.passenger_name,
                'ride_id': ride.ride_id, 
                'driver_id': ride.driver_id, 
                'passenger_id': ride.passenger_id, 
                'start_location': ride.start_location, 
                'drop_location': ride.drop_location, 
                'status': RideStatus(ride_metadata.ride_status).name, 
                'vehicle_id': ride_metadata.vehicle_id, 
                'vehicle_model': ride_metadata.vehicle_model, 
                'ride_otp': ride_metadata.ride_otp,
                'ride_fare': ride_metadata.ride_fare,
                'distance': ride_metadata.ride_distance,
                'ETR': ride_metadata.ride_ETR}

    @staticmethod
    def get_current_ride_passenger(passenger_id):
        query = session.query(Ride).join(RideMetadata, Ride.ride_id == RideMetadata.ride_id)        
        ride = query.filter(Ride.passenger_id == passenger_id, 
                            RideMetadata.ride_status.notin_([4, 5, 6])).first()
        if not ride:
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride.ride_id).first()
        return {'driver_name': ride_metadata.driver_name,
                'ride_id': ride.ride_id, 
                'driver_id': ride.driver_id, 
                'passenger_id': ride.passenger_id, 
                'start_location': ride.start_location, 
                'drop_location': ride.drop_location, 
                'status': RideStatus(ride_metadata.ride_status).name, 
                'vehicle_id': ride_metadata.vehicle_id, 
                'vehicle_model': ride_metadata.vehicle_model, 
                'ride_otp': ride_metadata.ride_otp,
                'ride_fare': ride_metadata.ride_fare,
                'distance': ride_metadata.ride_distance,
                'ETR': ride_metadata.ride_ETR}
    
    @staticmethod
    def passenger_cancel_ride(ride_id):
        ride = session.query(Ride).filter(Ride.ride_id == ride_id).first()
        if not ride:
            return None
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        if ride_metadata.ride_status not in [1,2] :
            return None
        ride_metadata.ride_status = int(RideStatus.PASSENGER_CANCELLED)
        session.commit()
        driver_vehicle = session.query(DriverVehicle).filter(DriverVehicle.driver_id == ride.driver_id).first()
        if driver_vehicle:
            driver_vehicle.driver_status = DriverStatus.WAITING
            session.commit()
        return ride_metadata.ride_id
    
    @staticmethod
    def rate_ride(ride_id, rating) : 
        ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride_id).first()
        if not ride_metadata : 
            return None
        if ride_metadata.ride_status != int(RideStatus.COMPLETED) :
            return None
        ride_metadata.ride_rating = rating
        session.commit()
        return ride_metadata.ride_id
    
    @staticmethod
    def ride_history(passenger_id):
        ##get all past rides for a passenger
        rides = session.query(Ride).join(RideMetadata, Ride.ride_id == RideMetadata.ride_id).filter(Ride.passenger_id == passenger_id, RideMetadata.ride_status == int(RideStatus.COMPLETED)).all()
        final_list = []
        for ride in rides :
            ride_metadata = session.query(RideMetadata).filter(RideMetadata.ride_id == ride.ride_id).first()
            final_list.append({'driver_name' :  ride_metadata.driver_name, 'ride_id': ride.ride_id, 'driver_id': ride.driver_id, 'start_location': ride.start_location, 'drop_location': ride.drop_location, 'status': RideStatus(ride_metadata.ride_status).name, 'vehicle_model': ride_metadata.vehicle_model, 'rating': ride_metadata.ride_rating,'fare':ride_metadata.ride_fare})
        return final_list
    
    '''Write methods for car pooling'''