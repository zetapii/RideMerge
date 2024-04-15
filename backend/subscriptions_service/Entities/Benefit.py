

class Benefit : 
    def __init__(self, 
                 apply_surge : bool, 
                 discount_rate : float,
                 safe_ride : bool,
                 premium_vehicle : bool,
                 ): 
        
        self.__id = id 
        self.__apply_surge = apply_surge
        self.__discount_rate = discount_rate
        self.__safe_ride = safe_ride
        self.__premium_vehicle = premium_vehicle

    def getId(self):
        return self.__id
    
    def setId(self, id):
        self.__id = id

    def getApplySurge(self):
        return self.__apply_surge
    
    def setApplySurge(self, apply_surge):
        self.__apply_surge = apply_surge

    def getDiscountRate(self):
        return self.__discount_rate
    
    def setDiscountRate(self, discount_rate):
        self.__discount_rate = discount_rate

    def getSafeRide(self):
        return self.__safe_ride
    
    def setSafeRide(self, safe_ride):
        self.__safe_ride = safe_ride

    def getPremiumVehicle(self):
        return self.__premium_vehicle
    
    def setPremiumVehicle(self, premium_vehicle):
        self.__premium_vehicle = premium_vehicle

    
    def __str__(self):
        return f'Benefit [id={self.__id},apply_surge={self.__apply_surge}, discount_rate={self.__discount_rate}, safe_ride={self.__safe_ride}, premium_vehicle={self.__premium_vehicle}]'
