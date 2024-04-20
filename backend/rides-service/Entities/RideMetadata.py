'''This will also store the speed of the vehicle maybe in ridemetadata'''
from enum import Enum 

import sys
sys.path.append('../../rides-service') 


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from Entities import base 

Base = base.Base 
class RideStatus(Enum):
    PENDING = 1     # NO DRIVER HAS ACCEPTED THE RIDE
    ACCEPTED = 2    # DRIVER HAS ACCEPTED THE RIDE
    PASSENGER_PICKED = 3    # PASSANGER HAS BEEN PICKED 
    DRIVER_CANCELLED = 4  # RIDE HAS BEEN CANCELLED BY DRIVER
    PASSENGER_CANCELLED = 5   # RIDE HAS BEEN CANCELLED BY RIDER
    COMPLETED = 6   # RIDE HAS BEEN COMPLETED

class RideMetadata(Base) :
    __tablename__ = 'RideMetadata'
    id = Column(String, primary_key=True)
    ride_id = Column(String)
    ride_otp = Column(String)
    ride_status = Column(Integer)
    ride_rating = Column(Integer)
    vehicle_id = Column(String)
    vehicle_model = Column(String)
    is_secure = Column(Boolean)
    driver_name = Column(String)
    passenger_name = Column(String)
    ride_fare = Column(Float)
    ride_ETR = Column(String)
    ride_distance = Column(Float)