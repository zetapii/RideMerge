import requests
import random
class RideService :
    BASE_URL_DRIVER = "http://127.0.0.1:5001/fetch/driver"
    BASE_URL_PASSENGER = "http://127.0.0.1:5001/fetch/passenger"
    BASE_URL_VEHICLE = "http://127.0.0.1:5001/fetch/vehicle"
    BASE_URL_SUBSCRIPTION = "http://127.0.0.1:5000/find_subscription_details"
    PER_KM_PRICE = 15
    SAFE_PRICE = 10
    PremiumMap = {'ModelA':50,'ModelB':40,'ModelC':30,'ModelD':20,'ModelE':10}

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
    
    ##IMPLEMENT THIS FUNCTION TOMRROW
    @staticmethod
    def get_routeistance(src,drop):
        return 100

    @staticmethod
    def get_fare(src, drop, model, passenger_id,is_safe = False):
        distance_in_km = RideService.get_routeistance(src, drop)
        fare = distance_in_km * RideService.PER_KM_PRICE
        premium_price = RideService.PremiumMap.get(model, 0)
        surge_price = random.randint(0, 10)

        response = requests.get(
            RideService.BASE_URL_SUBSCRIPTION,
            data={'userid': passenger_id}
        )

        add_to_fare = 0
        print("this is here")
        if response.status_code == 200 and response.json().get('message')=='OK':

            print("Response from subscription service")
            print(response.json())
            json_response = response.json()
            benefit_details = json_response['benefit_details']
            benefit_surge = benefit_details['apply_surge']
            benefit_premium = benefit_details['premium_vehicle']
            benefit_safe = benefit_details['safe_ride']
            discount_rate = benefit_details['discount_rate']
            
            if benefit_surge == False :
                add_to_fare += surge_price 
            if benefit_premium == False:
                add_to_fare += premium_price
            if benefit_safe == False and is_safe == True:
                add_to_fare += RideService.SAFE_PRICE 
            fare += add_to_fare
            fare -= (discount_rate * fare / 100)
        else:
            add_to_fare += premium_price
            add_to_fare += surge_price
            fare += add_to_fare
        return fare 
    
    @staticmethod
    def fetch_rides(src,dst,external_service):
        available_rides = external_service.fetch_rides(src,dst)
        return available_rides

