
class UserSavedLocations : 
    def __init__(self, id, userId, locationName, location):
        self.id = id
        self.userId = userId
        self.locationName = locationName
        self.locationAddress = location 
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getUserId(self):
        return self.userId
    
    def setUserId(self, userId):
        self.userId = userId
    
    def getLocationName(self):
        return self.locationName
    
    def setLocationName(self, locationName):
        self.locationName = locationName

    def getLocationAddress(self):
        return self.locationAddress
    
    def setLocationAddress(self, locationAddress):
        self.locationAddress = locationAddress

    def __str__(self) :
        return f"User ID: {self.userId}, Location Name: {self.locationName}, Location Address: {self.locationAddress}"