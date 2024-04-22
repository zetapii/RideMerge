import sys
sys.path.append('../../entitymanager-service')

import json
import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import UserDAO
from DAO import VehicleDAO
from DAO import DriverAdapter
from Entities import Driver
from Entities import Passenger

app = Flask(__name__)

from sqlalchemy.ext.declarative import DeclarativeMeta

Driver = Driver.Driver
Passenger = Passenger.Passenger


app = Flask(__name__)

import redis
# Connect to Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


def fetch_from_redis(key):
    try:
        vehicle_data = redis_client.get(key)
        if vehicle_data:
            return json.loads(vehicle_data)
        return None
    except redis.RedisError as e:
        print(f"Redis Error: {e}")
        return None

def cache_in_redis(key, data):
    try:
        redis_client.set(key, json.dumps(data, cls=AlchemyEncoder))
    except redis.RedisError as e:
        print(f"Redis Error: {e}")

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
    
@app.route('/register/driver', methods=['POST'])
def register_driver():
    try : 
        data = request.get_json()
        driver_adapter = DriverAdapter.DriverAdapter()
        driver_id = driver_adapter.create_user(data['name'], data['password'], data.get('email'), data['phone'],data['driving_license'])
        if driver_id:
            return jsonify({'driver_id': driver_id})
        else :
            return jsonify({'driver_id': None,'error':'error in registration'}), 400
    except Exception as e:
        return jsonify({'error':'error in registration','debug':str(e)}), 400

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    try : 
        data = request.get_json()
        user_dao = UserDAO.UserDAO()
        passenger_id = user_dao.create_user(Passenger,data['name'], data['password'], data.get('email'), data['phone'])
        return jsonify({'passenger_id' : passenger_id})
    except Exception as e:
        return jsonify({'error':'error in registration','debug':str(e)}), 400

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    try : 
        data = request.get_json()
        vehicle_id = VehicleDAO.VehicleDAO.add_vehicle(data['driver_id'], data['vehicle_model'], data['registration_number'], data['insurance_number'], data.get('manufacturer'), data.get('manufacturing_year'))
        if not vehicle_id:
            return jsonify({'vehicle_id' : None})
        return jsonify({'vehicle_id' : vehicle_id})
    except Exception as e:
        return jsonify({'error':'error in adding vehicle','debug':str(e)}), 400

@app.route('/login/passenger', methods=['POST'])
def login_passenger():
    try : 
        data = request.get_json()
        user_dao = UserDAO.UserDAO()
        passenger_id = user_dao.login_user(Passenger,data['phone'], data['password'])
        if not passenger_id:
            return jsonify({'user_id':None, 'token':None,'user_type':None})
        jwt_token = jwt.encode({'user_id' : passenger_id,'user_type':'passenger'}, 'secret', algorithm='HS256')
        return jsonify({'passenger_id':passenger_id, 'token' : jwt_token})
    except Exception as e:
        return jsonify({'error':'error in login','debug':str(e)}), 400

@app.route('/login/driver', methods=['POST'])
def login_driver():
    try : 
        data = request.get_json()
        user_dao = UserDAO.UserDAO()
        driver_id = user_dao.login_user(Driver,data['phone'],data['password'])
        if not driver_id:
            return jsonify({'user_id':None, 'token':None})
        jwt_token = jwt.encode({'user_id' : driver_id,'user_type':'driver'}, 'secret', algorithm='HS256')
        return jsonify({'driver_id' : driver_id,'token':jwt_token})
    except Exception as e:
        return jsonify({'error':'error in driver login','debug':str(e)})

@app.route('/verify/token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    try:
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        return jsonify({'user_id':decoded['user_id'], 'user_type':decoded['user_type']})
    except jwt.ExpiredSignatureError:
        return jsonify({'user_id':None, 'user_type':None,'error':'Token Expired'}), 400

@app.route('/fetch/driver/<id>', methods=['GET'])
def fetch_driver(id):
    try : 
        driver = fetch_from_redis('driver_' + id)
        if driver:
            return driver
        user_dao = UserDAO.UserDAO()
        driver = user_dao.get_user(Driver,id)
        if driver :
            cache_in_redis('driver_' + id, driver)
            return json.loads(json.dumps(driver, cls=AlchemyEncoder))
        else :
            return jsonify({'error': 'Id Not Found'}), 400
    except Exception as e:
        return jsonify({'error':'error in fetching driver','debug':str(e)}), 400


@app.route('/fetch/passenger/<id>', methods=['GET'])
def fetch_passenger(id):
    
    try :
        passenger = fetch_from_redis('passenger_' + id)
        if passenger:
            return passenger
        user_dao = UserDAO.UserDAO()
        passenger = user_dao.get_user(Passenger,id)
        if passenger: 
            cache_in_redis('passenger_' + id, passenger)
            return json.loads(json.dumps(passenger, cls=AlchemyEncoder))
        else :
            return jsonify({'error': 'Id Not Found'}), 400
    except Exception as e:
        return jsonify({'error':'error in fetching passenger','debug':str(e)}), 400
    
@app.route('/fetch/vehicle/<id>', methods=['GET'])
def fetch_vehicle(id):
    try : 
        vehicles = fetch_from_redis('vehicle_' + id)
        if vehicles:
            return vehicles
        vehicles = VehicleDAO.VehicleDAO.get_vehicle(id)
        if vehicles:
            cache_in_redis('vehicle_' + id, vehicles)
            return json.loads(json.dumps(vehicles, cls=AlchemyEncoder))
        else:
            return jsonify({'error': 'Id Not Found'}), 400
    except Exception as e:
        return jsonify({'error':'error in fetching vehicle','debug':str(e)}), 400
    
@app.route('/fetch/passengers', methods=['GET'])
def fetch_all_passengers():
    try :
        user_dao = UserDAO.UserDAO()
        passengers = user_dao.get_users(Passenger)
        if passengers:
            return json.loads(json.dumps(passengers, cls=AlchemyEncoder))
        else:
            return jsonify({'error': 'No passengers found'}), 400 
    except Exception as e:
        return jsonify({'error':'error in fetching passengers','debug':str(e)}), 400
    
@app.route('/fetch/drivers', methods=['GET'])
def fetch_all_drivers():
    try :
        user_dao = UserDAO.UserDAO()
        drivers = user_dao.get_users(Driver)
        if drivers:
            return json.loads(json.dumps(drivers, cls=AlchemyEncoder))
        else:
            return jsonify({'error': 'No drivers found'}), 400
    except Exception as e:
        return jsonify({'error':'error in fetching drivers','debug':str(e)}), 400
    
@app.route('/fetch/vehicles', methods=['GET'])
def fetch_all_vehicles():
    try :
        vehicles = VehicleDAO.VehicleDAO.get_vehicles()
        if vehicles:
            return json.loads(json.dumps(vehicles, cls=AlchemyEncoder))
        else:
            return jsonify({'error': 'No vehicles found'}), 400
    except Exception as e:
        return jsonify({'error':'error in fetching vehicles','debug':str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
