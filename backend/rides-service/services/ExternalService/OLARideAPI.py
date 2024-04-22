import sys
sys.path.append('/Users/zaid/Downloads/Software Engineering/SE-Project/se-project-3--_19/backend/rides-service/services/')

from ExternalService.interface.ExternalRideAPI import ExternalRideAPI
from RideService import RideService

class OLARideAPI(ExternalRideAPI):

    rides = [
        {
            'driver_name': 'OLA Driver 1',
            'vehicle_model': 'Honda City',
            'car_number': 'MH 12 1234',
            'rating': 4.5,
            'price': 100
        }
    ]
    
    TOKEN = None 
    def __init__(self, token):
        self.TOKEN = token

    def fetch_rides(self,source,destination):
        distance = RideService.get_routedistance(source,destination)
        for ride in self.rides:
            ride['distance'] = distance
        return self.rides
