

import requests
class RideService : 

    BASE_URL_DRIVER = "http://127.0.0.1:5001/fetch/driver"
    BASE_URL_PASSENGER = "http://127.0.0.1:5001/fetch/passenger"
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
        pass

    @staticmethod
    def get_routedistance(src,drop):
        pass

    @staticmethod
    def get_fare(src,drop,model):
        distanceInKM = RideService.get_routedistance(src,drop)
        fare = distanceInKM*RideService.PER_KM_PRICE
        if model in RideService.ModelMap:      
            fare += RideService.ModelMap[model]      
        return fare