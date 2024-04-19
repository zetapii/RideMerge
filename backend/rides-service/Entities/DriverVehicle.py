from enum import Enum 

import sys
sys.path.append('../../rides-services')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from Entities import base 

Base = base.Base 

class DriverStatus(Enum):
    DRIVING = 0
    WAITING = 1
    OFFLINE = 2
    
class DriverVehicle(Base) : 
    __tablename__ = 'DriverVehicle'
    id = Column(String, primary_key=True)
    driver_id = Column(String)
    vehicle_id = Column(String)
    driver_status = Column(Integer)
    current_location = Column(String)
    model = Column(String)