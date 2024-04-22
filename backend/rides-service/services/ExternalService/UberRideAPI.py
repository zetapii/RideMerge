import sys
sys.path.append('../../../../rides-services')

from ExternalService.interface.ExternalRideAPI import ExternalRideAPI
from RideService import RideService
class UberRideAPI(ExternalRideAPI):

    rides = [
        {
            'driver_name': 'UBER Driver 1',
            'car_model': 'Honda City',
            'car_number': 'MH 12 1234',
            'rating': 4.9,
            'price': 140
        }
    ]
    def __init__(self, token):
        self.TOKEN = token
    def fetch_rides(self,source,destination):
        distance = RideService.get_routedistance(source,destination)
        for ride in self.rides:
            ride['distance'] = distance
        return self.rides