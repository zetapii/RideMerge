from backend.subscriptions_service.DAO.Abstract.SubsBenefitDAOInterface import SubsBenefitDAOInterface

from backend.subscriptions_service.Entities.Benefit import Benefit


from backend.subscriptions_service.Entities.JSONFactory.Implementation.BenefitJSONFactory import BenefitJSONFactory


from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId


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
        
        self.__benefits.delete_one({
            '_id' : ObjectId(mongo_id),
        })

        return

    def update(self):

        self.__benefits.find_one_and_update({

        }, {

        })

        return

    def find(self,
             mongo_id = None):

        found = self.__benefits.find_one({
            '_id' : mongo_id,
        })

        if found == None:
            return found

        benefit = BenefitJSONFactory().convertToObject(json = found)

        return benefit