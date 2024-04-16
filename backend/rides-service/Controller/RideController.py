import sys
sys.path.append('../../services')

import json 
from sqlalchemy.ext.declarative import DeclarativeMeta
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import RideDAO
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

'''Fetch the Rides for the passenger From Start Location to End Location'''
'''This just fetches price and the models available'''

@app.route('/passenger/rides', methods=['GET']) 
def fetch_rides_passenger():
    #fetch basic details
    source = request.get_json()['source']
    destination = request.get_json()['destination']
    is_secure = request.get_json()['is_secure']
    available_rides = RideDAO.RideDAO.fetch_rides_passsenger(source, destination, is_secure)
    return jsonify(available_rides)
        

'''Parameters : user_id, Cab Model, Source, Destination, is_secure'''
@app.route('/passenger/match_ride', methods=['POST'])
def match_ride():
    pass 
    ##create a ride and set the status of the ride to 1 , showing that the user is interested in the ride
    ##ride object will be created here
    ##db involved -> Ride

'''Fetches All the rides requested by the passengers'''
#No parameters to be passed
@app.route('/driver/rides', methods=['GET'])
def fetch_rides_driver():
    ##db involved -> fetched from rides db where status is pending
    pass 

'''Accept the Ride for the Driver'''
#parameters to be passed are ride_id and drivervehicle_id 
@app.route('/driver/accept_ride', methods=['POST'])
def accept_ride_driver():
    pass 
    ##db involved -> Ride
    ##also push otp to user , thi is jut dummy for now

'''pickkup the passenger by the driver and otp is shared'''
'''Parameters to be passed are otp and ride_id'''
@app.route('/driver/pickup_passenger', methods=['POST'])
def pickup_passenger():
    pass
    ##pull otp from user
    ###db involved -> Ride
    ###just change the status of the ride to start

##parameter is just the ride id

@app.route('/passenger/complete_ride', methods=['POST']) ##complete ride completes the ride
def complete_ride():
    pass 
    #this will just mark the ride as completed and the passenger will be able to rate the driver
    ##db inovled -> Ride
    ##Just change the status to completed

##parameter is just the ride id
@app.route('/passenger/ride_fare', methods=['GET'])
def get_ride_fare():
    pass
    ##get the fare of the ride
    ##now the fare will be calculated based on the model, subscription of the user and the distance travelled
    ##db involved -> Ride and other microservices call

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

