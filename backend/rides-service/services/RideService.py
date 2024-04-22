import requests
import json
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
    
    @staticmethod
    def fetch_distance_details(source,destination):
        
        access_token = 'KRbBDs36XEs1DQ3fCFGTiDxVa8q0HKnwlQhezeXYaV2DNJnpc6Z7FGDpS9JutByl'

        origins = source
        destinations = destination

        url = f'https://api-v2.distancematrix.ai/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={access_token}'

        response = requests.get(url)

        try : 
            if response.status_code == 200:
                print("Request successful")
                print(json.dumps(response.json(), indent=4))  
                return response.json()['rows'][0]['elements'][0]['distance']['value'],response.json()['rows'][0]['elements'][0]['duration']['value']
        except Exception as e:
            print(f"Request failed with status code {response.status_code}")
        return None , None

    @staticmethod
    def get_routedistance(src,drop):
        distance,duration = RideService.fetch_distance_details(src,drop)
        return distance 
    
    @staticmethod
    def get_fare(src, drop, model, passenger_id,is_safe = False):
        distance_in_km = RideService.get_routedistance(src, drop)/1000
        fare = distance_in_km * RideService.PER_KM_PRICE
        premium_price = RideService.PremiumMap.get(model, 0)
        surge_price = random.randint(0, 10)

        response = requests.get(
            RideService.BASE_URL_SUBSCRIPTION,
            data={'userid': passenger_id}
        )

        add_to_fare = 0
        if response.status_code == 200 and response.json().get('message')=='OK':
            print("Response from subscription service")
            print(response.json())
            json_response = response.json()
            benefit_details = json_response.get('benefit_details')
            apply_surge = benefit_details.get('apply_surge')
            benefit_premium = benefit_details.get('premium_vehicle')
            benefit_safe = benefit_details.get('safe_ride')
            discount_rate = benefit_details.get('discount_rate')
            
            if benefit_details and apply_surge == True :
                add_to_fare += surge_price 
            if benefit_premium and benefit_premium == False:
                add_to_fare += premium_price
            if benefit_safe == False and is_safe == False:
                add_to_fare += RideService.SAFE_PRICE 
            fare += add_to_fare
            if discount_rate:
                fare -= (discount_rate * fare / 100)
        else:
            add_to_fare += premium_price
            add_to_fare += surge_price
            add_to_fare += RideService.SAFE_PRICE
            fare += add_to_fare
        return fare 
