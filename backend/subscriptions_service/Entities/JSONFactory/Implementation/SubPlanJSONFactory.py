from backend.subscriptions_service.Entities.JSONFactory.Abstract.JSONFactoryInterface import JSONFactoryInterface

from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan

class SubPlanJSONFactory(JSONFactoryInterface):

    def __init__(self):
        pass

    def convertToJSON(self,
                      subPlan : SubscriptionPlan):

        self.__json = dict()

        self.__json['userid']           = subPlan.getUserID()
        self.__json['benefit_id']       = subPlan.getBenefit()
        self.__json['price']            = subPlan.getPrice()
        self.__json['duration']         = subPlan.getDuration() 

        return self.__json

    def convertToObject(self, json : dict):
        try:
            id = json.get("_id", 0) 
            userid = json.get('userid', '')
            price = json.get("price", 0)
            duration = json.get("duration", 0)
            benefit  = json.get("benefit_id", '') 

            self.__sub = SubscriptionPlan(id = id,
                                          userid = userid,
                                          price = price,
                                          duration = duration,
                                          benefit_id = benefit)

            return self.__sub
        except Exception:
            return None