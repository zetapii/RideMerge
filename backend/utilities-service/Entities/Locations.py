import sys
from pymongo import MongoClient

sys.path.append('../../locations-service')
from Entities import base

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Locations'] 

locations_collection = db['Locations']

def insert_location(name):
    location_data = {"name": name}
    locations_collection.insert_one(location_data)

def fetch_location(name):
    return locations_collection.find_one({"name": name})

try:
    insert_location("Atlanta")

    fetched_location = fetch_location("Atlanta")

    print("Fetched Location:")
    print(fetched_location)
except Exception as e:
    print("Error:", e)
finally:
    client.close()
