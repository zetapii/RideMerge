import sys
# sys.path.append('../../Booking-Service')

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

'''Change the Status of the Driver-Vehicle Entity
OFFLINE
DRIVING
WAITING
'''

'''This will be used to change the status of the driver'''
@app.route('/driver/change_status', methods=['POST'])
#parameter to be passed is the driver_vehicle and the status
def change_status():
    ##db involved -> DriverVehicle
    pass

'''Fetch the Rides for the passenger From Start Location to End Location'''
'''This just fetches price and the models available'''
#parameters to be passed are user_id,source, destination, is_secure
@app.route('/passenger/rides', methods=['GET']) 
def fetch_rides_passenger():
    ##db involved -> fetched from DriverVehicle
    pass 

'''Parameters : Cab Model, Source, Destination, is_secure'''
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
    app.run(host='0.0.0.0', port=5001)