import sys
sys.path.append('../../entitymanager-service')

import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import EntityDAO
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
