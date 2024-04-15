from pymongo.mongo_client import MongoClient

from backend.subscriptions_service.DAO.Implementation.BenefitDAO import BenefitDAO
from backend.subscriptions_service.DAO.Implementation.SubscriptionDAO import SubscriptionDAO

from backend.subscriptions_service.Entities.JSONFactory.Implementation.BenefitJSONFactory import BenefitJSONFactory
from backend.subscriptions_service.Entities.JSONFactory.Implementation.SubPlanJSONFactory import SubPlanJSONFactory

from backend.subscriptions_service.Entities.Benefit import Benefit
from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan


from flask import Flask , request, json 


class SubscriptionController(object):
    """
    Class to control Subscription HTTP requests

    Arguments
    -------
    mongo_client : The mongo client of the database 
    
    """
    def __init__(self,
                 mongo_client : MongoClient): 
        
        self.__benefitdao = BenefitDAO(
            mongo_client = mongo_client
        )
        self.__subdao     = SubscriptionDAO(
            mongo_client = mongo_client
        )
        
        self.__benefitfactory = BenefitJSONFactory(
            
        )
        
        self.__subscriptionfactory = SubPlanJSONFactory(
            
        )
        
        self.__app = Flask(
            import_name = __name__
        )
        
        self.__app.add_url_rule(
            rule = '/add',
            view_func = self.__add_subscription,
        )
        
    
    def __add_subscription(self): 
        if request.method == 'GET':
            try:
                
                body = request.form 
                
                benefit = self.__benefitfactory.convertToObject(body)
                benefit_id = self.__benefitdao.add(benefit = benefit)

                body = dict(body) 
                body['benefit_id'] = str(benefit_id)

                subscription = self.__subscriptionfactory.convertToObject(body) 
                subscription_id = self.__subdao.add(subscription)

                res = {
                    'subscription_id' : str(subscription_id),
                }
            
                return self.__app.response_class(
                    response = json.dumps(res),
                    status = 200, 
                    mimetype = 'application/json'
                )
            
            except Exception as e:
                print(e) 
                return self.__app.response_class(
                    status = 400, 
                    mimetype = 'application/json' 
                )
        else:
            return 
    
    
    
    
    def runApp(self, port : int):
        self.__app.run(debug = True) 
    
    
    
    
        