class Location : 
    def __init__(self, id, name, latitude, longitude) :
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getLatitude(self):
        return self.latitude
    
    def setLatitude(self, latitude):
        self.latitude = latitude

    def getLongitude(self):
        return self.longitude
    
    def setLongitude(self, longitude):
        self.longitude = longitude

    def __str__(self) : 
        return f"Location [id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude}]"