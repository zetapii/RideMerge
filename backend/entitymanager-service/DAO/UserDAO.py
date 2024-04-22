import sys
sys.path.append('../../entitymanager-service')

import bcrypt

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

class UserDAO:
    def __init__(self):
        self.session = Session()

    def check_existing_phone(self, model_class, phone):
        user = self.session.query(model_class).filter(model_class.phone == phone).first()
        print(user)
        print("we are here ")
        return user

    def create_user(self, model_class, name, password, email, phone):
        if self.check_existing_phone(model_class, phone):
            return None
        user = model_class(id=str(uuid.uuid4()), name=name, password=password, email=email, phone=phone)
        self.session.add(user)
        self.session.commit()
        return user.id

    def login_user(self, model_class, phone, password):
        user = self.session.query(model_class).filter(model_class.phone == phone, model_class.password == password).first()
        if user:
            return user.id
        return None

    def get_user(self, model_class, id):
        user = self.session.query(model_class).filter(model_class.id == id).first()
        return user

    def get_users(self, model_class):
        users = self.session.query(model_class).all()
        return users 
    