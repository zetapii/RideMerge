from enum import Enum 

import sys
# sys.path.append('../../services')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
import base 

Base = base.Base 
class Vehicle(Base):
    __tablename__ = 'Vehicle'
    id = Column(String, primary_key=True)
    driver_id = Column(String)
    vehicle_model = Column(String)
    registration_number = Column(String)
    insurance_number = Column(String)
    manufacturer = Column(String)
    manufacturing_year = Column(Integer)