from backend.subscriptions_service.Entities.JSONFactory.Abstract.JSONFactoryInterface import JSONFactoryInterface

from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan

from datetime import date, datetime

class SubPlanJSONFactory(JSONFactoryInterface):

    def __init__(self):
        pass

    def convertToJSON(self,
                      subPlan : SubscriptionPlan):

        self.__json = dict()

        self.__json['userid']           = subPlan.getUserID()
        self.__json['benefit_id']       = subPlan.getBenefit()
        self.__json['duration']         = subPlan.getDuration() 
        self.__json['start_date']       = subPlan.getStartDate().strftime("%Y-%m-%d %H:%M:%S")
        self.__json['expiry_date']      = subPlan.getExpireDate().strftime("%Y-%m-%d %H:%M:%S") 
        return self.__json

    def convertToObject(self, json : dict):
        try:
            
            id = json.get("_id", 0) 
            
            userid = json.get('userid')
            
            
            duration = int(json.get("duration"))
            
            benefit  = json.get("benefit_id") 
    
            if json.get("start_date") is None: 
                start_date = None
            else:
                start_date = datetime.strptime(json.get("start_date"), "%Y-%m-%d %H:%M:%S").date()  
        
            self.__sub = SubscriptionPlan(id = id,
                                          userid = userid,
                                          duration = duration,
                                          benefit_id = benefit,
                                          start_date = start_date)

            return self.__sub
        except Exception as e:
            print(e) 
            return None