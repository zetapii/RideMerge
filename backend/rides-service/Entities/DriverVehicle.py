

##keep an enum for driving status which shows what the driver is doing currently
##like driving , waiting for a ride , offline etc
##This will be used to show the status of the driver in the frontend

from enum import Enum 

import sys
# sys.path.append('../../services')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
import base 

Base = base.Base 

class DriverStatus(Enum):
    DRIVING = 0
    WAITING = 2
    OFFLINE = 3
    
class DriverVehicle(Base) : 
    __tablename__ = 'DriverVehicle'
    id = Column(String, primary_key=True)
    driver_id = Column(String)
    vehicle_id = Column(String)
    driver_status = Column(Integer)
    current_location = Column(String)
    model = Column(String)