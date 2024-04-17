from enum import Enum 

import sys
sys.path.append('../../rides-services')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from Entities import base 

Base = base.Base 

class Ride(Base):
    __tablename__ = 'Ride'
    ride_id = Column(String, primary_key=True)
    driver_id = Column(String)
    passenger_id = Column(String)
    start_location = Column(String)
    drop_location = Column(String)

