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

from DAO import UserDAO
from services import EntityService

Driver = Driver.Driver
Vehicle = Vehicle.Vehicle
UserDAO = UserDAO.UserDAO

class DriverAdapter():
    def create_user(self, name, password, email, phone, driving_license):
        user_dao = UserDAO()
        driver_id = user_dao.create_user(Driver, name, password, email, phone)
        if driver_id:
            driver = user_dao.get_user(Driver, driver_id)
            driver.driving_license = driving_license
            user_dao.session.commit()
        return driver_id