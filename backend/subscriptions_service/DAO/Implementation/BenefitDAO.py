from backend.subscriptions_service.DAO.Abstract.SubsBenefitDAOInterface import SubsBenefitDAOInterface

from backend.subscriptions_service.Entities.Benefit import Benefit


from backend.subscriptions_service.Entities.JSONFactory.Implementation.BenefitJSONFactory import BenefitJSONFactory


from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

from bson import json_util
import json
class BenefitDAO(SubsBenefitDAOInterface):

    """
        DAO Object corresponding to the Benefit

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
        self.__benefits = self.__db['benefits']


    def add(self,
            benefit : Benefit):

        if benefit == None: 
            return None 
        benefit_json = BenefitJSONFactory().convertToJSON(benefit)

        retval = self.__benefits.insert_one(benefit_json)

        return retval.inserted_id

    def remove(self,
               mongo_id = None,
               id = None):
        try:
            self.__benefits.delete_one({
            '_id' : ObjectId(mongo_id),
            })
            return True 

        except Exception as e:
            print(e)
            return False

    def update(self,
               mongo_id : str,
               apply_surge = None, 
               discount_rate = None, 
               premium_vehicle = None, 
               safe_ride = None):
        
        update = dict() 
        
        if apply_surge is not None:
            update['apply_surge'] = apply_surge
        
        if discount_rate is not None:
            update['discount_rate'] = discount_rate
            
        if premium_vehicle is not None:
            update['premium_vehicle'] = premium_vehicle
        
        if safe_ride is not None:
            update['safe_ride'] = safe_ride
        
        update = {"$set": update}
        
        try:
            self.__benefits.find_one_and_update({
            '_id' : ObjectId(mongo_id)
            }, update)
            
            return True 

        except Exception as e:
            print(e)
            return False


    def find(self,
             userid = None,
             mongo_id = None):

        filter = dict()
        if userid is not None:
            filter['userid'] = userid 
        
        if mongo_id is not None:
            filter['_id'] = ObjectId(mongo_id) 
        
        found = self.__benefits.find_one(filter)
        if found == None:
            return found

        benefit = BenefitJSONFactory().convertToObject(json = found)

        return benefit
    
    def findAll(self):

        found = self.__benefits.find()
        if found == None:
            return None
        benefits = []
        for benefit in found:
            print(benefit)
            ##get __id mongo id
            benefits.append(json.loads(json_util.dumps(benefit)))
            # benefits.append({})

        return benefits