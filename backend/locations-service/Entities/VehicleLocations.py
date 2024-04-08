import datetime 

class VehicleLocations : 
    def __init__(self, id, vehicle_id, location) :
        self.id = id
        self.vehicle_id = vehicle_id
        self.location = location
        self.speed = 0
        self.last_updated = datetime.datetime.now()

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getVehicleId(self):
        return self.vehicle_id
    
    def setVehicleId(self, vehicle_id):
        self.vehicle_id = vehicle_id

    def getLocation(self):
        return self.location
    
    def setLocation(self, location):
        self.location = location

    def getSpeed(self):
        return self.speed
    
    def setSpeed(self, speed):
        self.speed = speed
    
    def getLastUpdated(self):
        return self.last_updated

    def setLastUpdated(self, last_updated):
        self.last_updated = last_updated
    
    def __str__(self) :
        return f"Vehicle Location [id={self.id}, vehicle_id={self.vehicle_id}, location={self.location}, speed={self.speed}, last_updated={self.last_updated}]"    
