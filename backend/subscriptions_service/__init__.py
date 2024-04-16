from pymongo import mongo_client
from pymongo.mongo_client import MongoClient
from pymongo.server_api   import ServerApi

from backend.subscriptions_service.Entities.Benefit import Benefit

from backend.subscriptions_service.DAO.Implementation.BenefitDAO import BenefitDAO

from backend.subscriptions_service.Controller.SubscriptionController import SubscriptionController

from flask import Flask 

username = 'amanrajmathematics'
password = 'aman404butfound'


uri = \
f'mongodb+srv://{username}:{password}\
@clusterdeployement.r4rrwfv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDeployement'

client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    controller = SubscriptionController(
        mongo_client= client
    )
    
    controller.runApp(port = 6000)  
    

except Exception as e:
    print("WARNING : Please connect to Internet before proceeding")
    print(e)