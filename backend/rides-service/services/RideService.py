

import requests
class RideService :
    BASE_URL_DRIVER = "http://127.0.0.1:5001/fetch/driver"
    BASE_URL_PASSENGER = "http://127.0.0.1:5001/fetch/passenger"
    BASE_URL_VEHICLE = "http://127.0.0.1:5001/fetch/vehicle"
    BASE_URL_SUBSCRIPTION = "http://127.0.0.1:5000/find_subscription_details"
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
    def get_fare(src,drop,model, passenger_id):
        return 100
        pass
        distanceInKM = RideService.get_routedistance(src,drop)
        fare = distanceInKM*RideService.PER_KM_PRICE
        premium_price = 0
        if model in RideService.ModelMap:      
            premium_price = RideService.ModelMap[model]

        surge_price = 0
        ##surge_price don't add if user is subscribed
        response = requests.get(RideService.BASE_URL_SUBSCRIPTION, data= {
            'userid' : passenger_id,
        }) 
        
        add_to_fare = 0
        if response.status_code == 200:
            json_response = response.json() 
            
            if json_response['message'] == 'OK':
                benefit_surge = json_response['benefit_details']['apply_surge'] 
                benefit_premium = json_response['benefit_details']['premium_vehicle']
                discount_rate = json_response['benefit_details']['discount_rate']
                if benefit_surge == False:
                    add_to_fare += 100
                if benefit_premium == False :
                    add_to_fare += premium_price
                fare+=add_to_fare
                fare-=(discount_rate*fare/100)                 
            else: 
                add_to_fare+=premium_price
                add_to_fare+=surge_price
                fare+=add_to_fare
            
        return fare + add_to_fare 
    

    @staticmethod
    def fetch_rides(src,dst,external_service):
        available_rides = external_service.fetch_rides(src,dst)
        return available_rides
