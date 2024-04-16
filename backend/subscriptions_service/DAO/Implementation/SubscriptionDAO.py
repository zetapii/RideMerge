from backend.subscriptions_service.DAO.Abstract.SubsBenefitDAOInterface import SubsBenefitDAOInterface

from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan
from backend.subscriptions_service.Entities.JSONFactory.Implementation.SubPlanJSONFactory import SubPlanJSONFactory

from pymongo.mongo_client import MongoClient

from bson.objectid import ObjectId


class SubscriptionDAO(SubsBenefitDAOInterface):
    """
        DAO Object corresponding to the Subscription

        Parameters
        -------
        mongo_client : Mongo Client to the database

        Operations
        -------
        Supports all the CRUD operations
    """
    def __init__(self,
                 mongo_client : MongoClient):

        self.__db = mongo_client['database']
        self.__benefits = self.__db['subscriptions']

    def add(self,
            benefit : SubscriptionPlan):

        benefit_json = SubPlanJSONFactory().convertToJSON(benefit)

        retval = self.__benefits.insert_one(benefit_json)

        return retval.inserted_id

    def remove(self,
               mongo_id = None,
               userid = None):

        delete_target = self.__benefits.find_one({
            'userid' : userid,
        })
        
        if delete_target == None:
            return None 
        
        id = str(delete_target.get('benefit_id')) 
        
        self.__benefits.delete_one({
            'userid' : userid,
        })
        
        return id


    def update(self,
               userid : str,
               new_start_date = None,
               new_duration = None):
        update = dict()
        
        if new_start_date is not None: 
            update['start_date'] = new_start_date
        
        if new_duration is not None:
            update['duration'] = new_duration
        
        update =  {"$set": update}
        try:
            found = self.__benefits.find_one({'userid' : userid})['benefit_id'] 
            self.__benefits.find_one_and_update({
                'userid' : userid
            }, update)
            return {
                'updated' : True,
                'benefit' : found
            }
        
        except Exception as e:
            print(e)
            return {
                'updated' : False,
                
            }
        


    def find(self,
             userid = None,
             mongo_id = None):

        filter = dict()
        
        if mongo_id is not None:
            filter['_id'] = ObjectId(mongo_id)
        if userid is not None:
            filter['userid'] = userid 
            
        found = self.__benefits.find_one(filter) 

        if found == None:
            return found

        benefit = SubPlanJSONFactory().convertToObject(found)

        return benefit