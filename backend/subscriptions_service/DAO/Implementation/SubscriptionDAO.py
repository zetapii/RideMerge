from backend.subscriptions_service.DAO.Abstract.SubsBenefitDAOInterface import SubsBenefitDAOInterface

from backend.subscriptions_service.Entities.SubscriptionPlan import SubscriptionPlan
from backend.subscriptions_service.Entities.JSONFactory.Implementation.SubPlanJSONFactory import SubPlanJSONFactory

from pymongo.mongo_client import MongoClient



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
               id = None):

        self.__benefits.delete_one(filter={
            '_id' : mongo_id,
            'id' : id,
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

        benefit = SubPlanJSONFactory().convertToObject(found)

        return benefit