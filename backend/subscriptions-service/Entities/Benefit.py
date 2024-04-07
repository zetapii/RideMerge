

class Benefit : 
    def __init__(self, id, name, description, apply_surge , discount_rate,safe_ride,premium_vehicle) : 
        self.id = id
        self.name = name
        self.description = description
        self.apply_surge = apply_surge
        self.discount_rate = discount_rate
        self.safe_ride = safe_ride
        self.premium_vehicle = premium_vehicle

    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getDescription(self):
        return self.description
    
    def setDescription(self, description):
        self.description = description

    def getApplySurge(self):
        return self.apply_surge
    
    def setApplySurge(self, apply_surge):
        self.apply_surge = apply_surge

    def getDiscountRate(self):
        return self.discount_rate
    
    def setDiscountRate(self, discount_rate):
        self.discount_rate = discount_rate

    def getSafeRide(self):
        return self.safe_ride
    
    def setSafeRide(self, safe_ride):
        self.safe_ride = safe_ride

    def getPremiumVehicle(self):
        return self.premium_vehicle
    
    def setPremiumVehicle(self, premium_vehicle):
        self.premium_vehicle = premium_vehicle

    
    def __str__(self):
        return f'Benefit [id={self.id}, name={self.name}, description={self.description}, apply_surge={self.apply_surge}, discount_rate={self.discount_rate}, safe_ride={self.safe_ride}, premium_vehicle={self.premium_vehicle}]'
