

class Benefit(object):
    """
    DTO Object for Benefits in the Subscription Plan of the User
    
    Parameters
    -------
    apply_surge : Whether to apply surge or not
    discount_rate : Rate of discount to be applied to the user 
    safe_ride : Whether user is registered for safe ride or not 
    premium_vehicle : Whether user is registered for premium vehicle or not 
    """ 
    def __init__(self, 
                 apply_surge : bool, 
                 discount_rate : float,
                 safe_ride : bool,
                 premium_vehicle : bool,
                 price : float
                 ): 
        
        self.__id = id 
        self.__apply_surge = apply_surge
        self.__discount_rate = discount_rate
        self.__safe_ride = safe_ride
        self.__premium_vehicle = premium_vehicle
        self.__price = price

    def getId(self):
        return self.__id
    
    def setId(self, id : str):
        self.__id = id

    def getApplySurge(self):
        return self.__apply_surge
    
    def setApplySurge(self, apply_surge : bool):
        self.__apply_surge = apply_surge

    def getDiscountRate(self):
        return self.__discount_rate
    
    def setDiscountRate(self, discount_rate : float):
        self.__discount_rate = discount_rate

    def getSafeRide(self):
        return self.__safe_ride
    
    def setSafeRide(self, safe_ride : bool):
        self.__safe_ride = safe_ride

    def getPremiumVehicle(self):
        return self.__premium_vehicle
    
    def setPremiumVehicle(self, premium_vehicle : bool):
        self.__premium_vehicle = premium_vehicle 

    def getPrice(self):
        return self.__price
    
    def setPrice(self, price : float):
        self.__price = price
    def __str__(self):
        return f'Benefit [id={self.__id},apply_surge={self.__apply_surge}, discount_rate={self.__discount_rate}, safe_ride={self.__safe_ride}, premium_vehicle={self.__premium_vehicle}]'
