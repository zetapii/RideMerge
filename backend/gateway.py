import json
import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from functools import wraps

app = Flask(__name__)

BASE_URL_ENTITY = 'http://localhost:5001/'
BASE_URL_RIDE = 'http://localhost:5002/'

@app.route('/register/driver', methods=['POST'])
def register_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'register/driver', json=data)
    return jsonify(response.json())

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'register/passenger', json=data)
    return jsonify(response.json())

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'driver/add_vehicle', json=data)
    return jsonify(response.json())

@app.route('/login/passenger', methods=['POST'])
def login_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'login/passenger', json=data)
    return jsonify(response.json())

@app.route('/login/driver', methods=['POST'])
def login_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'login/driver', json=data)
    return jsonify(response.json())

@app.route('/fetch/driver/<id>', methods=['GET'])
def fetch_driver(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/driver/' + id)
    return jsonify(response.json())

@app.route('/fetch/passenger/<id>', methods=['GET'])
def fetch_passenger(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/passenger/' + id)
    return jsonify(response.json())

@app.route('/fetch/vehicle/<id>', methods=['GET'])
def fetch_vehicle(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/vehicle/' + id)
    return jsonify(response.json())

@app.route('/fetch/passengers', methods=['GET'])
def fetch_all_passengers():
    response = requests.get(BASE_URL_ENTITY + 'fetch/passengers')
    return jsonify(response.json())

@app.route('/fetch/drivers', methods=['GET'])
def fetch_all_drivers():
    response = requests.get(BASE_URL_ENTITY + 'fetch/drivers')
    return jsonify(response.json())

@app.route('/fetch/vehicles', methods=['GET'])
def fetch_all_vehicles():
    response = requests.get(BASE_URL_ENTITY + 'fetch/vehicles')
    return jsonify(response.json())

@app.route('/fetch/driver_vehicles/<driver_id>', methods=['GET'])
def fetch_driver_vehicle(driver_id):
    response = requests.get(BASE_URL_RIDE + 'fetch/driver_vehicles/' + driver_id)
    return jsonify(response.json())

@app.route('/driver/driver_vehicle',methods=['POST'])
def add_driver_vehicle():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/driver_vehicle', json=data)
    return jsonify(response.json())

@app.route('/driver/change_status', methods=['POST'])
def change_status():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/change_status', json=data)
    return jsonify(response.json())

@app.route('/passenger/rides', methods=['POST'])
def fetch_rides_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/rides', json=data)
    return jsonify(response.json())

@app.route('/passenger/book_ride', methods=['POST'])
def book_ride():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/book_ride', json=data)
    return jsonify(response.json())

@app.route('/driver/rides/<driver_id>', methods=['GET'])
def fetch_rides_driver(driver_id):
    response = requests.get(BASE_URL_RIDE + 'driver/rides/' + driver_id)
    return jsonify(response.json())

@app.route('/ride_details/<id>', methods=['GET'])
def get_ride_details(id):
    response = requests.get(BASE_URL_RIDE + 'ride_details/' + id)
    return jsonify(response.json())

@app.route('/driver/accept_ride', methods=['POST'])
def accept_ride_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/accept_ride', json=data)
    return jsonify(response.json())

@app.route('/driver/pickup_passenger', methods=['POST'])
def pickup_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/pickup_passenger', json=data)
    return jsonify(response.json())

@app.route('/driver/complete_ride', methods=['POST'])
def complete_ride():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/complete_ride', json=data)
    return jsonify(response.json())

@app.route('/passenger/ride_fare/<id>', methods=['GET'])
def get_ride_fare(id):
    response = requests.get(BASE_URL_RIDE + 'passenger/ride_fare/' + id)
    return jsonify(response.json())

@app.route('/driver/current_ride/<driver_id>', methods=['GET'])
def get_current_ride_driver(driver_id):
    response = requests.get(BASE_URL_RIDE + 'driver/current_ride/' + driver_id)
    return jsonify(response.json())

@app.route('/passenger/current_ride/<passenger_id>', methods=['GET'])
def get_current_ride_passenger(passenger_id):
    response = requests.get(BASE_URL_RIDE + 'passenger/current_ride/' + passenger_id)
    return jsonify(response.json())

@app.route('/passenger/rate_ride', methods=['POST'])
def rate_ride_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/rate_ride', json=data)
    return jsonify(response.json())

@app.route('/passenger/ride_history/<passenger_id>', methods=['GET'])
def fetch_ride_history_passenger(passenger_id):
    response = requests.get(BASE_URL_RIDE + 'passenger/ride_history/' + passenger_id)
    return jsonify(response.json())

@app.route('/passenger/cancel_ride', methods=['POST'])
def cancel_ride_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/cancel_ride', json=data)
    return jsonify(response.json())

@app.route('/driver/cancel_ride', methods=['POST'])
def cancel_ride_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/cancel_ride', json=data)
    return jsonify(response.json())

@app.route('/fetch/external/rides', methods=['POST'])
def fetch_external_rides():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'fetch/external/rides', json=data)
    return jsonify(response.json())

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'pong'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005,debug=True)
