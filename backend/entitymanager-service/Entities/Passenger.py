from enum import Enum 

import sys
# sys.path.append('../../services')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
import base 

Base = base.Base 
class Passenger(Base):
    __tablename__ = 'Passenger'
    id = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)
    