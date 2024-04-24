import json
import jwt
from enum import Enum
from flask import Flask, jsonify, request
import requests
from functools import wraps

app = Flask(__name__)

BASE_URL_ENTITY = 'http://localhost:5001/'
BASE_URL_RIDE = 'http://localhost:5002/'
BASE_URL_SUBSCRIPTION = 'http://localhost:5010/'
BASE_URL_PAYMENT = "http://10.2.130.75:5014/"


import redis

redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

def record(resp) :
    # status = resp.get('status')
    return 
    if resp.get('error') :
        print("Error occured")
        cnt_errors = redis_client.get('cnt_errors')
        if cnt_errors:
            redis_client.set('cnt_errors', int(cnt_errors)+1)
        else:
            redis_client.set('cnt_errors', 1)

def authenticate(request):
    jwt = request.get_jons().get('Authorization')
    response = requests.post(BASE_URL_ENTITY + 'verify/token', json={'token': jwt})
    if response.status_code == 200:
        return True
    else:
        return False 
    
@app.route('/register/driver', methods=['POST'])
def register_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'register/driver', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/register/passenger', methods=['POST'])
def register_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'register/passenger', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'driver/add_vehicle', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/login/passenger', methods=['POST'])
def login_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'login/passenger', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/login/driver', methods=['POST'])
def login_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_ENTITY + 'login/driver', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/driver/<id>', methods=['GET'])
def fetch_driver(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/driver/' + id)
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/passenger/<id>', methods=['GET'])
def fetch_passenger(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/passenger/' + id)
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/vehicle/<id>', methods=['GET'])
def fetch_vehicle(id):
    response = requests.get(BASE_URL_ENTITY + 'fetch/vehicle/' + id)
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/passengers', methods=['GET'])
def fetch_all_passengers():
    response = requests.get(BASE_URL_ENTITY + 'fetch/passengers')
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/drivers', methods=['GET'])
def fetch_all_drivers():
    response = requests.get(BASE_URL_ENTITY + 'fetch/drivers')
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/vehicles', methods=['GET'])
def fetch_all_vehicles():
    response = requests.get(BASE_URL_ENTITY + 'fetch/vehicles')
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/driver_vehicles/<driver_id>', methods=['GET'])
def fetch_driver_vehicle(driver_id):
    response = requests.get(BASE_URL_RIDE + 'fetch/driver_vehicles/' + driver_id)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/driver_vehicle',methods=['POST'])
def add_driver_vehicle():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/driver_vehicle', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/change_status', methods=['POST'])
def change_status():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/change_status', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/rides', methods=['POST'])
def fetch_rides_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/rides', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/book_ride', methods=['POST'])
def book_ride():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/book_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/rides/<driver_id>', methods=['GET'])
def fetch_rides_driver(driver_id):
    response = requests.get(BASE_URL_RIDE + 'driver/rides/' + driver_id)
    record(response.json())
    return jsonify(response.json())

@app.route('/ride_details/<id>', methods=['GET'])
def get_ride_details(id):
    response = requests.get(BASE_URL_RIDE + 'ride_details/' + id)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/accept_ride', methods=['POST'])
def accept_ride_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/accept_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/pickup_passenger', methods=['POST'])
def pickup_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/pickup_passenger', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/complete_ride', methods=['POST'])
def complete_ride():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/complete_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/ride_fare/<id>', methods=['GET'])
def get_ride_fare(id):
    response = requests.get(BASE_URL_RIDE + 'passenger/ride_fare/' + id)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/current_ride/<driver_id>', methods=['GET'])
def get_current_ride_driver(driver_id):
    response = requests.get(BASE_URL_RIDE + 'driver/current_ride/' + driver_id)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/current_ride/<passenger_id>', methods=['GET'])
def get_current_ride_passenger(passenger_id):
    response = requests.get(BASE_URL_RIDE + 'passenger/current_ride/' + passenger_id)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/rate_ride', methods=['POST'])
def rate_ride_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/rate_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/ride_history/<passenger_id>', methods=['GET'])
def fetch_ride_history_passenger(passenger_id):
    response = requests.get(BASE_URL_RIDE + 'passenger/ride_history/' + passenger_id)
    record(response.json())
    return jsonify(response.json())

@app.route('/passenger/cancel_ride', methods=['POST'])
def cancel_ride_passenger():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'passenger/cancel_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/driver/cancel_ride', methods=['POST'])
def cancel_ride_driver():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'driver/cancel_ride', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/fetch/external/rides', methods=['POST'])
def fetch_external_rides():
    data = request.get_json()
    response = requests.post(BASE_URL_RIDE + 'fetch/external/rides', json=data)
    record(response.json())
    return jsonify(response.json())

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'pong'})

###SUBSCRIPTION SERVICE STARTS HERE
@app.route('/add', methods=['GET'])
def add_subscription():
    form = request.form
    response = requests.get(BASE_URL_SUBSCRIPTION + 'add', data=form) 
    record(response.json())
    return jsonify(response.json())

@app.route('/find_subscription', methods=['GET'])
def find_subscription():
    form = request.form
    response = requests.get(BASE_URL_SUBSCRIPTION + 'find_subscription', data=form)
    record(response.json())
    return jsonify(response.json())

@app.route('/find_subscription_details', methods=['GET'])
def find_subscription_benefits():
    form = request.form
    response = requests.get(BASE_URL_SUBSCRIPTION + 'find_subscription_details', data=form)
    record(response.json())
    return jsonify(response.json())

@app.route('/get_benefit', methods=['GET'])
def get_benefit():
    response = requests.get(BASE_URL_SUBSCRIPTION + 'get_benefit')
    record(response.json())
    return jsonify(response.json())

@app.route('/delete', methods=['GET'])
def delete_subscription():
    form = request.form
    response = requests.get(BASE_URL_SUBSCRIPTION + 'delete', data=form)
    record(response.json())
    return jsonify(response.json())

###SUBSCRIPTION SERVICE ENDS HERE

# PAYMENT SERVICE
@app.route('/creditcard', methods = ['POST'])
def pay_with_creditcard():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'creditcard', json=data)
    return jsonify(response.json())

@app.route('/debitcard', methods = ['POST'])
def pay_with_debitcard():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'debitcard', json=data)
    return jsonify(response.json())

@app.route('/upi', methods = ['POST'])
def pay_with_upi():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'upi', json=data)
    return jsonify(response.json())

# PAYMENT SERVICE
@app.route('/creditcard', methods = ['POST'])
def pay_with_creditcard():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'creditcard', json=data)
    return jsonify(response.json())

@app.route('/debitcard', methods = ['POST'])
def pay_with_debitcard():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'debitcard', json=data)
    return jsonify(response.json())

@app.route('/upi', methods = ['POST'])
def pay_with_upi():
    data = request.get_json()
    response = requests.post(BASE_URL_PAYMENT + 'upi', json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005,debug=True)
