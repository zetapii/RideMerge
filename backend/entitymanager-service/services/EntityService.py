
import requests



class EntityService : 
    BASE_URL_DRIVERVEHICLE = "http://127.0.0.1:5002/driver/driver_vehicle"

    @staticmethod
    def create_driver_vehicle(driver_id,vehicle_id): 
        data = {
            "driver_id": driver_id,
            "vehicle_id": vehicle_id
        }
        response = requests.post(EntityService.BASE_URL_DRIVERVEHICLE, json=data)
        if response.status_code == 200:
            return response.json()
        else :
            return None