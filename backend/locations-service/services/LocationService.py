'''This will return the Driver's updated location , when the driver is on a ride.'''
'''How? This can be done by fetching from gps but for simulating what we can do is we can use the speed of the driver and the time he started the ride to calculate the distance he has travelled and then update the location accordingly.'''


import datetime
from math import radians, sin, cos, sqrt, atan2

class LocationService:
    def __init__(self):
        self.vehicle_locations = {}

    def getVehicleLocation(self, vehicle_id):
        return self.vehicle_locations.get(vehicle_id)

    def updateVehicleLocation(self, vehicle_id, vehicle_location):
        self.vehicle_locations[vehicle_id] = vehicle_location

    def updateVehicleSpeed(self, vehicle_id, speed):
        if vehicle_id in self.vehicle_locations:
            self.vehicle_locations[vehicle_id].setSpeed(speed)
            self.vehicle_locations[vehicle_id].setLastUpdated(datetime.datetime.now())

    def updateVehicleLastUpdated(self, vehicle_id, last_updated):
        if vehicle_id in self.vehicle_locations:
            self.vehicle_locations[vehicle_id].setLastUpdated(last_updated)

    def getVehicleLocationHistory(self, vehicle_id):
        # Not implemented for this example
        pass

    def getVehicleLocationHistoryByTime(self, vehicle_id, start_time, end_time):
        # Not implemented for this example
        pass

    def getVehicleLocationHistoryByDistance(self, vehicle_id, distance):
        # Not implemented for this example
        pass

    def simulateVehicleLocationUpdate(self, vehicle_id, start_time, current_time):
        if vehicle_id not in self.vehicle_locations:
            return None
        
        vehicle_location = self.vehicle_locations[vehicle_id].getLocation()
        speed = self.vehicle_locations[vehicle_id].getSpeed()

        # Calculate distance traveled based on speed and time elapsed
        time_difference = current_time - start_time
        time_difference_seconds = time_difference.total_seconds()
        distance_traveled = speed * time_difference_seconds

        # Update latitude and longitude based on distance traveled
        # For simplicity, we'll move the vehicle northward (increasing latitude)
        # and eastward (increasing longitude) assuming a constant speed.
        # This is just a basic example and should be adjusted based on actual requirements.
        latitude = vehicle_location.getLatitude() + (distance_traveled / 111000)  # 1 degree of latitude is approximately 111 kilometers
        longitude = vehicle_location.getLongitude() + (distance_traveled / (111000 * cos(radians(vehicle_location.getLatitude()))))  # Adjusted for latitude

        # Update vehicle location
        new_location = Location(vehicle_location.getId(), vehicle_location.getName(), latitude, longitude)
        self.vehicle_locations[vehicle_id].setLocation(new_location)
        self.vehicle_locations[vehicle_id].setLastUpdated(current_time)

# Example usage:
# Assuming vehicle_id, start_time, and current_time are properly defined
# location_service = LocationService()
# location_service.simulateVehicleLocationUpdate(vehicle_id, start_time, current_time)
