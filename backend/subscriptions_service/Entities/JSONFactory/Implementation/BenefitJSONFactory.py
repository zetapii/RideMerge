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
            surge  = eval(json.get('apply_surge'))
            disc   = json.get('discount_rate',type = float)
            safe   = eval(json.get('safe_ride'))
            premium= eval(json.get('premium_vehicle'))

            benefit = Benefit(
                
                apply_surge = surge,
                discount_rate = disc,
                safe_ride = safe,
                premium_vehicle = premium
            )

            return benefit

        except KeyError:
            return None