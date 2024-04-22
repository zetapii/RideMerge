from pymongo.mongo_client import MongoClient

from backend.subscriptions_service.DAO.Implementation.BenefitDAO      import BenefitDAO
from backend.subscriptions_service.DAO.Implementation.SubscriptionDAO import SubscriptionDAO

from backend.subscriptions_service.Entities.JSONFactory.Implementation.BenefitJSONFactory import BenefitJSONFactory
from backend.subscriptions_service.Entities.JSONFactory.Implementation.SubPlanJSONFactory import SubPlanJSONFactory

from backend.subscriptions_service.Entities.Benefit          import Benefit
from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan

from datetime import date 
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
        
        self.__benefitdao = BenefitDAO(mongo_client = mongo_client)
        self.__subdao     = SubscriptionDAO(mongo_client = mongo_client)
        
        self.__benefitfactory = BenefitJSONFactory()
        self.__subscriptionfactory = SubPlanJSONFactory()
        
        self.__app = Flask(
            import_name = __name__
        )
        
        self.__app.add_url_rule(
            rule = '/add',
            view_func = self.__add_subscription,
        )
        
        self.__app.add_url_rule(
            rule = '/delete',
            view_func = self.__remove_subscription,
        )
        
        self.__app.add_url_rule(
            rule = '/find_subscription',
            view_func = self.__find_subscription,
        )
        
        self.__app.add_url_rule(
            rule = '/find_subscription_details',
            view_func = self.__find_subscription_benefits,
        )
        
        self.__app.add_url_rule(
            rule = '/check_expiry',
            view_func = self.__check_if_subscription_expired,
        )
        
        self.__app.add_url_rule(
            rule = '/renew_subscription',
            view_func = self.__renew_subscription,
        )

        self.__app.add_url_rule(
            rule = '/add_benefit',
            view_func = self.__add_benefit,
        )    

        self.__app.add_url_rule(
            rule = '/get_benefit',
            view_func = self.__get_benefit,
        )

    def runApp(self, port : int):
        self.__app.run(host='0.0.0.0',port = 5010 ,debug = True)
    
    # 405 
    def generateIncorrectRequest(self):
        res = {
            'message' : 'Request not allowed, use GET only' 
        }
        return self.__app.response_class(
            response = json.dumps(res),
            status = 405, 
            mimetype = 'application/json',
        )
    
    # 400
    def badRequest(self, e):
        print(e) 
        res = {
            'message' : 'Bad Request',
        }
        
        return self.__app.response_class(
            response = json.dumps(res),
            status = 400, 
            mimetype = 'application/json',
        )
    
    # 200 
    def sendResponse(self, response):
        return self.__app.response_class(
            response = json.dumps(response),
            status = 200, 
            mimetype = 'application/json',
        )
         
    
    def __add_subscription(self): 
        if request.method == 'GET':
            try:
                body = request.form                 
                subscription = self.__subscriptionfactory.convertToObject(body) 
                subscription_id = self.__subdao.add(subscription)
                if subscription_id == None:
                    return self.sendResponse({
                        'message' : 'SubscriptionAlreadyExists',
                    })
                return self.sendResponse({
                    'message' : 'OK',
                    'subscription_id' : str(subscription_id),
                })
            
            except Exception as e:
                return self.badRequest(e) 
        else:
            return self.generateIncorrectRequest()
    
    
    def __remove_subscription(self):
        if request.method == 'GET':
            try: 
              userid = request.form.get("userid") 
              benefit_id = self.__subdao.remove(userid = userid) 
              
              return self.sendResponse({
                  'message' : 'OK',
                
              })
            except Exception as e: 
                return self.badRequest(e) 
        else: 
            return self.generateIncorrectRequest()
     
     
    def __find_subscription(self):
        if request.method == 'GET':
            try: 
                userid = request.form.get("userid") 
                
                subscription = self.__subdao.find(userid = userid)
                
                if subscription == None: 
                    return self.sendResponse({
                        'message' : 'Not Found',
                    })
                
                json_sub = self.__subscriptionfactory.convertToJSON(subscription) 
                
                return self.sendResponse({
                    'message' : 'OK',
                    'subscription_details' : json_sub,
                })
                
            except Exception as e: 
                return self.badRequest(e) 
            
        else:
            return self.generateIncorrectRequest()
    
    def __find_subscription_benefits(self):
        if request.method == 'GET':
            try: 
                userid = request.form.get("userid") 
                subscription = self.__subdao.find(userid = userid)
                
                if subscription == None: 
                    return self.sendResponse({
                        'message' : 'Not Found',
                    })
                if subscription.checkExpired() == True: 
                    return self.sendResponse({
                        'message' : 'expired',
                    })
                    
                benefit_id = subscription.getBenefit() 
                
                benefit = self.__benefitdao.find(mongo_id = benefit_id)  
                
                json_benefit = self.__benefitfactory.convertToJSON(benefit) 
                
                return self.sendResponse({
                    'message' : 'OK',
                    'benefit_details' : json_benefit,
                })
                
            except Exception as e: 
                return self.badRequest(e) 
            
        else:
            return self.generateIncorrectRequest()
    
    def __check_if_subscription_expired(self):
        if request.method == 'GET':
            try: 
                userid = request.form.get("userid") 
                subscription = self.__subdao.find(userid = userid)
                
                if subscription == None: 
                    return self.sendResponse({
                        'message' : 'Not Found',
                    })
                isExpired = subscription.checkExpired() 
                
                return self.sendResponse({
                    'message' : 'OK',
                    'isExpired' : isExpired,
                })
            except Exception as e: 
                return self.badRequest(e) 
        else: 
           return self.generateIncorrectRequest()
    
    ## 
    def __renew_subscription(self):
        if request.method == 'GET':
            try: 
                userid = request.form.get("userid") 
                new_duration = request.form.get("new_duration")
                new_price = request.form.get("new_price")
                    
                transaction = self.__subdao.update(userid = userid, 
                                     new_duration = new_duration,
                                     new_price = new_price)
                
                if transaction['updated'] == False:
                    return self.sendResponse({
                        'message' : 'OK',
                        'renewed' : False,
                        })
                
                transaction2 = self.__benefitdao.update(mongo_id = transaction['benefit'],
                                                        apply_surge = request.form.get("apply_surge"),
                                                        discount_rate = request.form.get("discount_rate"),
                                                        premium_vehicle = request.form.get("premium_vehicle"),
                                                        safe_ride = request.form.get("safe_ride")) 
                
                return self.sendResponse({
                    'message' : 'OK',
                    'renewed' : transaction2,
                })
            except Exception as e: 
                return self.badRequest(e) 
        else: 
           return self.generateIncorrectRequest()
    
    def __add_benefit(self):
        if request.method == 'GET':
            try: 
                print(request.form)
                benefit = self.__benefitfactory.convertToObject(request.form) 
                print("got  here")
                benefit_id = self.__benefitdao.add(benefit = benefit)
                
                return self.sendResponse({
                    'message' : 'OK',
                    'benefit_id' : str(benefit_id),
                })
            except Exception as e: 
                return self.badRequest(e) 
        else: 
            return self.generateIncorrectRequest()

    def __get_benefit(self):
        if request.method == 'GET':
            try: 

                benefits = self.__benefitdao.findAll() 
                
                return self.sendResponse({
                    'message' : 'OK',
                    'benefits' : benefits,
                })
            except Exception as e: 
                return self.badRequest(e) 
        else: 
            return self.generateIncorrectRequest()

