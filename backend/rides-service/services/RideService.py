

import requests
class RideService : 

    BASE_URL_DRIVER = "http://127.0.0.1:5001/fetch/driver"
    BASE_URL_PASSENGER = "http://127.0.0.1:5001/fetch/passenger"
    BASE_URL_VEHICLE = "http://127.0.0.1:5001/fetch/vehicle"
    
    PER_KM_PRICE = 15
    ModelMap = {'ModelA':50,'ModelB':40,'ModelC':30}
    @staticmethod
    def fetch_passenger_details(id) : 
        response = requests.get(f"{RideService.BASE_URL_PASSENGER}/{id}")
        return response.json()
    
    @staticmethod
    def fetch_driver_details(id):
        response = requests.get(f"{RideService.BASE_URL_DRIVER}/{id}")
        return response.json()

    @staticmethod
    def fetch_vehicles_detail(id):
        response = requests.get(f"{RideService.BASE_URL_VEHICLE}/{id}")
        print(response.json())
        return response.json()
    
    @staticmethod
    def get_routedistance(src,drop):
        ##Do Actual Implementation
        return 100

    @staticmethod
    def get_fare(src,drop,model):
        distanceInKM = RideService.get_routedistance(src,drop)
        fare = distanceInKM*RideService.PER_KM_PRICE
        if model in RideService.ModelMap:      
            fare += RideService.ModelMap[model]
        ##surge_price don't add if user is subscribed

        return fare
    
# RideService.fetch_vehicles_detail("6e39e675-53be-4f5b-b44c-f870046a8134")

