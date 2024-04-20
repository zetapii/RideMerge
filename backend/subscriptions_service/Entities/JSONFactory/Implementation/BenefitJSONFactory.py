from backend.subscriptions_service.Entities.JSONFactory.Abstract.JSONFactoryInterface import JSONFactoryInterface

from backend.subscriptions_service.Entities.Benefit import Benefit

class BenefitJSONFactory(JSONFactoryInterface):

    def __init__(self):
        pass

    def convertToJSON(self,
                      benefit : Benefit):
        self.__json = dict()
        
        self.__json['apply_surge']      = benefit.getApplySurge()
        self.__json['discount_rate']    = benefit.getDiscountRate()
        self.__json['safe_ride']        = benefit.getSafeRide()
        self.__json['premium_vehicle']  = benefit.getPremiumVehicle()
        self.__json['price']            = benefit.getPrice()
        return self.__json

    def convertToObject(self,
                         json : dict):
        try:
            surge = json.get("apply_surge")
            if type(surge) == type(str):
                surge  = eval(json.get('apply_surge'))
            
            disc   = float(json.get('discount_rate'))
            
            safe = json.get("safe_ride")
            if type(safe) == type(str):
                safe  = eval(json.get('safe_ride'))
            
            premium = json.get("premium_vehicle")
            if type(surge) == type(str):
                premium  = eval(json.get('premium_vehicle'))

            price = float(json.get("price"))

            benefit = Benefit(
                
                apply_surge = surge,
                discount_rate = disc,
                safe_ride = safe,
                premium_vehicle = premium,
                price = price
            )

            return benefit

        except KeyError:
            return None