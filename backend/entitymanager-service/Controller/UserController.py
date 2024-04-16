import sys
sys.path.append('../../services')

#import jwt thingy
import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import UserDAO
app = Flask(__name__)

@app.route('/register/driver', methods=['POST'])
def register_driver():
    driver = request.get_json()
    driver_id = UserDAO.UserDAO.create_driver(driver['data'])
    return jsonify({'driver_id' : driver_id})

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    passenger = request.get_json()
    passenger_id = UserDAO.UserDAO.create_passenger(passenger['data'])
    return jsonify({'passenger_id' : passenger_id})

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    driver_id = request.get_json()['driver_id']
    vehicle = request.get_json()['vehicle']
    UserDAO.UserDAO.add_vehicle_to_driver(driver_id, vehicle)
    return jsonify({'status' : 'success'})

@app.route('/login/user', methods=['POST'])
def login_user():
    user = request.get_json()
    user_id = UserDAO.UserDAO.login_user(user['data'])
    jwt_token = jwt.encode({'user_id' : user_id}, 'secret', algorithm='HS256')
    return jsonify({'token' : jwt_token})

@app.route('/login/driver', methods=['POST'])
def login_driver():
    driver = request.get_json()
    driver_id = UserDAO.UserDAO.login_driver(driver['data'])
    jwt_token = jwt.encode({'driver_id' : driver_id}, 'secret', algorithm='HS256')
    return jsonify({'driver_id' : jwt_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

