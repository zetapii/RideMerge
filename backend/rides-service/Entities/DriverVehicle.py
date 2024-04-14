

##keep an enum for driving status which shows what the driver is doing currently
##like driving , waiting for a ride , offline etc
##This will be used to show the status of the driver in the frontend

from enum import Enum

class DriverStatus(Enum):
    DRIVING = 0
    WAITING = 2
    OFFLINE = 3

class DriverVehicle : 
    def __init__(self, id , driver_id, vehicle_id):
        self.id = id
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.driver_status = None 
        self.current_location = None