
from interfaces import User

class Driver(User):

    def __init__(self, id, passsword, name, dob , mobile, email,licence_, current_vehicle,availablity_status):
        super().__init__(id, passsword, name, dob , mobile, email)
        self.license = licence_
        self.current_vehicle = current_vehicle
        self.availablity_status = availablity_status    

    def getLicense(self):
        return self.license
    
    def setLicense(self, license):
        self.license = license
    
    def getCurrentVehicle(self):
        return self.current_vehicle
    
    def setCurrentVehicle(self, vehicle):
        self.current_vehicle = vehicle

    def getAvailablityStatus(self):
        return self.availablity_status
    
    def setAvailablityStatus(self, status):
        self.availablity_status = status

    def __str__(self):
        return f'Driver [id={self.id}, name={self.name}, dob={self.dob}, mobile={self.mobile}, email={self.email}, license={self.license}, current_vehicle={self.current_vehicle}, availablity_status={self.availablity_status}]'
