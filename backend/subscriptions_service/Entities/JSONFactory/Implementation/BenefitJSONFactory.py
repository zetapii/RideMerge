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
        return self.__json

    def convertToObject(self,
                         json : dict):
        try:
            surge  = json.get('apply_surge', type = bool)
            disc   = json.get('discount_rate',type = float)
            safe   = json.get('safe_ride', type = bool)
            premium= json.get('premium_vehicle',type = bool)

            benefit = Benefit(
                
                apply_surge = surge,
                discount_rate = disc,
                safe_ride = safe,
                premium_vehicle = premium
            )

            return benefit

        except KeyError:
            return None