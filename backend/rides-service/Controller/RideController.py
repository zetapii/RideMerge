import sys
sys.path.append('../../rides-service')

import json 
from sqlalchemy.ext.declarative import DeclarativeMeta
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import RideDAO
from services import RideService

app = Flask(__name__)

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

class DriverStatus(Enum):
    DRIVING = 0
    WAITING = 1
    OFFLINE = 2

@app.route('/fetch/driver_vehicle/<id>', methods=['GET'])
def fetch_driver_vehicle(id):
    driver_vehicle = RideDAO.RideDAO.get_drivervehicle(id)
    if driver_vehicle != None:
        return json.dumps(driver_vehicle, cls=AlchemyEncoder)

@app.route('/driver/driver_vehicle',methods=['POST'])
def add_driver_vehicle():
    driver_id = request.get_json()['driver_id']
    vehicle_id = request.get_json()['vehicle_id']
    
    model = request.get_json()['model']
    if RideDAO.RideDAO.create_drivervehicle(driver_id, vehicle_id, None , model) != None:
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failure'})

@app.route('/driver/change_status', methods=['POST'])
def change_status():
    driver_id = request.get_json()['driver_id']
    status = request.get_json()['status']
    if RideDAO.RideDAO.change_status(driver_id, status) != None:
        return jsonify({'status' : 'success'})
    else:   
        return jsonify({'status' : 'failure'})
    
@app.route('/passenger/rides', methods=['GET']) 
def fetch_rides_passenger():
    source = request.get_json()['source']
    destination = request.get_json()['destination']
    is_secure = request.get_json()['is_secure']
    available_rides = RideDAO.RideDAO.fetch_rides_passsenger(source, destination, is_secure)
    return jsonify(available_rides)
        
@app.route('/passenger/match_ride', methods=['POST'])
def match_ride():
    ride_id = RideDAO.RideDAO.match_ride(request.get_json()['passenger_id'], request.get_json()['source'], request.get_json()['destination'], request.get_json()['is_secure'], request.get_json()['vehicle_model'])
    return jsonify({'ride_id':ride_id})

'''Fetches All the rides requested by the passengers'''
@app.route('/driver/rides/<id>', methods=['GET'])
def fetch_rides_driver():
    rides = RideDAO.RideDAO.fetch_rides_driver(id)
    return json.loads(json.dumps(rides, cls=AlchemyEncoder))


@app.route('/driver/accept_ride', methods=['POST'])
def accept_ride_driver():
    ride_id = request.get_json()['ride_id']
    drivervehicle_id = request.get_json()['drivervehicle_id']
    if RideDAO.RideDAO.accept_ride_driver(ride_id, drivervehicle_id) != None:
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failure'})

@app.route('/driver/pickup_passenger', methods=['POST'])
def pickup_passenger():
    ride_id = request.get_json()['ride_id']
    otp = request.get_json()['otp']
    if RideDAO.RideDAO.pickup_passenger(ride_id, otp) != None:
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failure'})
##parameter is just the ride id

@app.route('/passenger/complete_ride', methods=['POST']) 
def complete_ride():
    ride_id = request.get_json()['ride_id']
    if RideDAO.RideDAO.complete_ride(ride_id) != None:
        return jsonify({'status' : 'success'})
    else :
        return jsonify({'status' : 'failure'})
    
@app.route('/passenger/ride_fare/<id>', methods=['GET'])
def get_ride_fare(id):
    ride_details = RideDAO.RideDAO.get_ride_details(id)
    if ride_details == None:
        return jsonify({'fare':None})
    fare = RideService.RideService.get_fare(ride_details.start_location,ride_details.drop_location,ride_details.vehicle_model)
    return jsonify({'fare':fare})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)