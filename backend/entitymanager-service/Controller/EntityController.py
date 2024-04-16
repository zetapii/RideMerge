import sys
sys.path.append('../../services')

import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import UserDAO
app = Flask(__name__)

@app.route('/register/driver', methods=['POST'])
def register_driver():
    driver = request.get_json()
    driver_id = UserDAO.UserDAO.create_driver(driver['data'].name, driver['data'].password, driver['data'].email, driver['data'].phone, driver['data'].driving_license)
    return jsonify({'driver_id' : driver_id})

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    passenger = request.get_json()
    passenger_id = UserDAO.UserDAO.create_passenger(passenger['data'].name, passenger['data'].password, passenger['data'].email, passenger['data'].phone)
    return jsonify({'passenger_id' : passenger_id})

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    driver_id = request.get_json()['driver_id']
    vehicle = request.get_json()['vehicle']
    vehicle_id = UserDAO.UserDAO.add_vehicle(driver_id, vehicle['vehicle_model'], vehicle['registration_number'], vehicle['insurance_number'], vehicle['manufacturer'], vehicle['manufacturing_year'])
    return jsonify({'status' : vehicle_id})

@app.route('/login/passenger', methods=['POST'])
def login_passenger():
    passenger = request.get_json()
    passenger_id = UserDAO.UserDAO.login_passenger(passenger['data'].phone, passenger['data'].password)
    jwt_token = jwt.encode({'passenger_id' : passenger_id}, 'secret', algorithm='HS256')
    return jsonify({'passenger_id':passenger_id, 'token' : jwt_token})

@app.route('/login/driver', methods=['POST'])
def login_driver():
    driver = request.get_json()
    driver_id = UserDAO.UserDAO.login_driver(driver['data'].phone,driver['data'].password)
    jwt_token = jwt.encode({'driver_id' : driver_id}, 'secret', algorithm='HS256')
    return jsonify({'driver_id' : driver_id,'token':jwt_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
