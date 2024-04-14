from enum import Enum

class RideStatus(Enum):
    PENDING = 1     # NO DRIVER HAS ACCEPTED THE RIDE
    ACCEPTED = 2    # DRIVER HAS ACCEPTED THE RIDE
    PASSENGER_PICKED = 3    # PASSANGER HAS BEEN PICKED 
    DRIVER_CANCELLED = 4  # RIDE HAS BEEN CANCELLED
    RIDER_CANCELLED = 5   # RIDE HAS BEEN CANCELLED
    COMPLETED = 6   # RIDE HAS BEEN COMPLETED

class Ride:
    def __init__(self, ride_id, driver_id, passenger_id, start_location, drop_location , status):
        self.ride_id = ride_id
        self.driver_id = driver_id
        self.passenger_id = passenger_id
        self.start_location = start_location
        self.drop_location = drop_location
