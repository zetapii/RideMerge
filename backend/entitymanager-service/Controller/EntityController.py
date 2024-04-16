import sys
sys.path.append('../../entitymanager-service')

import json
import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import EntityDAO
app = Flask(__name__)

from sqlalchemy.ext.declarative import DeclarativeMeta

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
    data = request.get_json()
    driver_id = EntityDAO.EntityDAO.create_driver(data['name'], data['password'], data['email'], data['phone'], data['driving_license'])
    return jsonify({'driver_id' : driver_id})

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    data = request.get_json()
    passenger_id = EntityDAO.EntityDAO.create_passenger(data['name'], data['password'], data['email'], data['phone'])
    return jsonify({'passenger_id' : passenger_id})

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle_id = EntityDAO.EntityDAO.add_vehicle(data['driver_id'], data['vehicle_model'], data['registration_number'], data['insurance_number'], data['manufacturer'], data['manufacturing_year'])
    return jsonify({'status' : vehicle_id})

@app.route('/login/passenger', methods=['POST'])
def login_passenger():
    data = request.get_json()
    passenger_id = EntityDAO.EntityDAO.login_passenger(data['phone'], data['password'])
    if not passenger_id:
        return jsonify({'passenger_id':None, 'token':None})
    jwt_token = jwt.encode({'passenger_id' : passenger_id}, 'secret', algorithm='HS256')
    return jsonify({'passenger_id':passenger_id, 'token' : jwt_token})

@app.route('/login/driver', methods=['POST'])
def login_driver():
    data = request.get_json()
    driver_id = EntityDAO.EntityDAO.login_driver(data['phone'],data['password'])
    if not driver_id:
        return jsonify({'driver_id':None, 'token':None})
    jwt_token = jwt.encode({'driver_id' : driver_id}, 'secret', algorithm='HS256')
    return jsonify({'driver_id' : driver_id,'token':jwt_token})

@app.route('/fetch/driver/<id>', methods=['GET'])
def fetch_driver(id):
    driver = EntityDAO.EntityDAO.get_driver(id)
    if driver : 
        return json.loads(json.dumps(driver, cls=AlchemyEncoder))
    else :
        return jsonify({'error': 'Id Not Found'}), 400
    
@app.route('/fetch/passenger/<id>', methods=['GET'])
def fetch_passenger(id):
    passenger = EntityDAO.EntityDAO.get_passenger(id)
    if passenger: 
        return json.loads(json.dumps(passenger, cls=AlchemyEncoder))
    else :
        return jsonify({'error': 'Id Not Found'}), 400
    
@app.route('/fetch/vehicles/<id>', methods=['GET'])
def fetch_vehicle(id):
    vehicles = EntityDAO.EntityDAO.get_vehicle(id)
    if vehicles:
        return json.loads(json.dumps(vehicles, cls=AlchemyEncoder))
    else:
        return jsonify({'error': 'Id Not Found'}), 400
    
@app.route('/fetch/passengers', methods=['GET'])
def fetch_all_passengers():
    passengers = EntityDAO.EntityDAO.get_passengers()
    if passengers:
        return json.loads(json.dumps(passengers, cls=AlchemyEncoder))
    else:
        return jsonify({'error': 'No vehicles found'}), 400

@app.route('/fetch/drivers', methods=['GET'])
def fetch_all_drivers():
    drivers = EntityDAO.EntityDAO.get_drivers()
    if drivers:
        return json.loads(json.dumps(drivers, cls=AlchemyEncoder))
    else:
        return jsonify({'error': 'No vehicles found'}), 400

@app.route('/fetch/vehicles', methods=['GET'])
def fetch_all_vehicles():
    vehicles = EntityDAO.EntityDAO.get_vehicles()
    if vehicles:
        return json.loads(json.dumps(vehicles, cls=AlchemyEncoder))
    else:
        return jsonify({'error': 'No vehicles found'}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
