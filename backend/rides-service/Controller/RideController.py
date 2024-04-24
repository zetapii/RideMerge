import sys
sys.path.append('../../rides-service')

import json 
from sqlalchemy.ext.declarative import DeclarativeMeta
from enum import Enum
from flask import Flask, jsonify, request
import requests
from DAO import RideDAO
from services import RideService
from enum import IntEnum
from services.ExternalService.factory import ExternalRideFactory

ExternalRideFactory = ExternalRideFactory.ExternalRideFactory 

app = Flask(__name__)

import redis
# Connect to Redis
redis_host = 'localhost'
redis_port = 6380
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

def invalidate_redis_keys(keys):
    try:
        redis_client.delete(*keys)
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

class DriverStatus(IntEnum):
    DRIVING = 0
    WAITING = 1
    OFFLINE = 2


@app.route('/fetch/driver_vehicles/<driver_id>', methods=['GET'])
def fetch_driver_vehicle(driver_id):
    driver_vehicle = RideDAO.RideDAO.get_drivervehicle(driver_id)
    if driver_vehicle != None:
        return json.loads(json.dumps(driver_vehicle, cls=AlchemyEncoder))
    else : 
        return jsonify({'driver_vehicle':None})

@app.route('/driver/driver_vehicle',methods=['POST'])
def add_driver_vehicle():
    driver_id = request.get_json()['driver_id']
    vehicle_id = request.get_json()['vehicle_id']    
    if RideDAO.RideDAO.create_drivervehicle(driver_id, vehicle_id) != None:
        return jsonify({'status' : 'success'})
    else:
        return jsonify({'status' : 'failure'})
    
@app.route('/driver/change_status', methods=['POST'])
def change_status():
    driver_vehicleid = request.get_json()['driver_vehicleid']
    status = request.get_json()['status']
    if status == 'WAITING':
        status = int(DriverStatus.WAITING)
    elif status == 'DRIVING':
        status = int(DriverStatus.DRIVING)
    else : 
        status = int(DriverStatus.OFFLINE)
    if RideDAO.RideDAO.change_status(driver_vehicleid, status) != None:
        return jsonify({'status' : 'success'})
    else:   
        return jsonify({'status' : 'failure','error':'error occured'})
    
@app.route('/passenger/rides', methods=['POST']) 
def fetch_rides_passenger():
    try :
        source = request.get_json()['source']
        destination = request.get_json()['destination']
        is_secure = request.get_json()['is_secure']
        passenger_id = request.get_json()['passenger_id']
        available_rides = RideDAO.RideDAO.fetch_rides_passsenger(source, destination, is_secure,passenger_id)
        return jsonify(available_rides)
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/passenger/book_ride', methods=['POST'])
def book_ride():
    try :
        ride_id = RideDAO.RideDAO.book_ride(request.get_json()['passenger_id'], request.get_json()['source'], request.get_json()['destination'], request.get_json()['is_secure'], request.get_json()['vehicle_model'], request.get_json().get('is_latlan'))
        if ride_id == None:
            return jsonify({'error':'error in booking ride'})
        return jsonify({'ride_id':ride_id})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/driver/rides/<driver_id>', methods=['GET'])
def fetch_rides_driver(driver_id):
    try : 
        rides = RideDAO.RideDAO.fetch_rides_driver(driver_id)
        return rides
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/ride_details/<id>', methods=['GET'])
def get_ride_details(id):
    try : 
        ride_details = RideDAO.RideDAO.get_ride_details(id)
        if not ride_details:
            return jsonify({'ride_details':None})
        return json.loads(json.dumps(ride_details, cls=AlchemyEncoder))
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/driver/accept_ride', methods=['POST'])
def accept_ride_driver():
    try : 
        ride_id = request.get_json()['ride_id']
        drivervehicle_id = request.get_json()['driver_id']
        if RideDAO.RideDAO.accept_ride_driver(ride_id, drivervehicle_id) != None:
            ride = RideDAO.RideDAO.get_ride_details(ride_id)
            invalidate_redis_keys(['passenger_current_ride_' + ride['passenger_id'], 'driver_current_ride_' + ride['driver_id']])
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failure'})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/driver/pickup_passenger', methods=['POST'])
def pickup_passenger():
    try : 
        ride_id = request.get_json()['ride_id']
        otp = request.get_json()['otp']
        if RideDAO.RideDAO.pickup_passenger(ride_id, otp) != None:
            ride = RideDAO.RideDAO.get_ride_details(ride_id)
            invalidate_redis_keys(['passenger_current_ride_' + ride['passenger_id'], 'driver_current_ride_' + ride['driver_id']])
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failure'})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})
    
@app.route('/driver/complete_ride', methods=['POST']) 
def complete_ride():
    try : 
        ride_id = request.get_json()['ride_id']
        if RideDAO.RideDAO.complete_ride(ride_id) != None:
            ride = RideDAO.RideDAO.get_ride_details(ride_id)
            invalidate_redis_keys(['passenger_current_ride_' + ride['passenger_id'], 'driver_current_ride_' + ride['driver_id']])
            return jsonify({'status' : 'success'})
        else :
            return jsonify({'status' : 'failure','error':'error occured'})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})
    
@app.route('/passenger/ride_fare/<id>', methods=['GET'])
def get_ride_fare(id):
    try : 
        ride_details = RideDAO.RideDAO.get_ride_details(id)
        print(ride_details)
        if ride_details == None:
            return jsonify({'fare':None,'error':'error in fetching ride details'})
        fare = RideService.RideService.get_fare(ride_details['start_location'],ride_details['drop_location'],ride_details['vehicle_model'],ride_details['passenger_id'],ride_details['is_secure'])
        return jsonify({'fare':fare})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/driver/current_ride/<driver_id>', methods=['GET'])
def get_current_ride_driver(driver_id):
    try : 
        ride = fetch_from_redis('driver_current_ride_' + driver_id)
        if ride:
            return ride
        ride = RideDAO.RideDAO.get_current_ride_driver(driver_id)
        if not ride : 
            return jsonify({'ride':None,'error':'error occured'})
        cache_in_redis('driver_current_ride_' + driver_id, ride)
        return json.loads(json.dumps(ride, cls=AlchemyEncoder))
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/passenger/current_ride/<passenger_id>', methods=['GET'])
def get_current_ride_passenger(passenger_id):
    try : 
        ride = fetch_from_redis('passenger_current_ride_' + passenger_id)
        if ride:
            return ride
        ride = RideDAO.RideDAO.get_current_ride_passenger(passenger_id)
        if not ride : 
            return jsonify({'ride':None,'status':'NORIDE'})
        cache_in_redis('passenger_current_ride_' + passenger_id, ride)
        return json.loads(json.dumps(ride, cls=AlchemyEncoder))
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/passenger/cancel_ride', methods=['POST'])
def cancel_ride_passenger():
    try : 
        ride_id = request.get_json()['ride_id']
        if RideDAO.RideDAO.passenger_cancel_ride(ride_id) != None:
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failure'})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})

@app.route('/passenger/rate_ride', methods=['POST'])
def rate_ride_passenger():
    try : 
        ride_id = request.get_json()['ride_id']
        rating = request.get_json()['rating']
        if RideDAO.RideDAO.rate_ride(ride_id, rating) != None:
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failure'})
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})
    
@app.route('/passenger/ride_history/<passenger_id>', methods=['GET'])
def fetch_ride_history_passenger(passenger_id):
    try : 
        rides = RideDAO.RideDAO.ride_history(passenger_id)
        if not rides:
            return jsonify([])
        return json.loads(json.dumps(rides, cls=AlchemyEncoder))
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})
    
@app.route('/fetch/external/rides', methods=['POST'])
def fetch_external_rides():
    try : 
        source = request.get_json()['source']
        destination = request.get_json()['destination']
        platform = request.get_json()['platform']
        available_rides = external_ride_factory.get_ride_service(platform).fetch_rides(source, destination)
        return jsonify(available_rides)
    except Exception as e:
        return jsonify({'error':'error occured' , 'debug':str(e)})
    
if __name__ == '__main__':
    global external_ride_factory
    external_ride_factory = ExternalRideFactory("TOKEN")
    app.run(host='0.0.0.0', port=5002,debug=True)