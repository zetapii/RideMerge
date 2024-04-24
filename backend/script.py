import requests


BASE_URL_ENTITY = "http://127.0.0.1:5001/"

def register():
    
    data = {
        'name': 'driver1',
        'password': 'driver1',
        'email': 'driver1',
        'phone' :'7992381519',
        'driving_license': '123456789'
    }
    response1 = requests.post(BASE_URL_ENTITY + 'register/driver', json=data)
    driver_id = response1.json().get('driver_id')
    print(response1.json())
    data = {
        'name': 'passenger1',
        'password': 'passenger1',
        'email': 'passenger1',
        'phone' :'9198776090',
    }
    response = requests.post(BASE_URL_ENTITY + 'register/passenger', json=data)
    print(response.json())
    passenger_id = response1.json().get('passenger_id')
    data = {
        'driver_id': response1.json()['driver_id'],
        'vehicle_model': 'swift',
        'registration_number': 'HYD12345',
        'insurance_number': 'MYINSURANCENUMBER',
        'manufacturer': 'HONDA',
        'manufacturing_year': '2021'
    }
    response = requests.post(BASE_URL_ENTITY + 'driver/add_vehicle', json=data)
    print(response.json())
    print(driver_id," ",passenger_id)
    return response.json().get('driver_id') 

def main():
    ##just fetch the driver vehicles from this 
    ##@app.route('/fetch/driver_vehicle/<id>', methods=['GET'])

    BASE_URL = "http://127.0.0.1:5002/"
    ''''
    @app.route('/driver/driver_vehicle',methods=['POST'])
    def add_driver_vehicle():
        driver_id = request.get_json()['driver_id']
        vehicle_id = request.get_json()['vehicle_id']    
        if RideDAO.RideDAO.create_drivervehicle(driver_id, vehicle_id) != None:
            return jsonify({'status' : 'success'})
        else:
            return jsonify({'status' : 'failure'})
    '''
    data = {
        'driver_id': 'ed767a53-44f0-4611-862d-c82290834d66',
        'vehicle_id': '6e39e675-53be-4f5b-b44c-f870046a8134'
    }
    response = requests.post(BASE_URL + 'driver/driver_vehicle', json=data)
    print(response.json())


def test_monitoring():
    for i in range(100):
        data = {
            'password': 'driver1',
            'email': 'driver1',
            'phone' :'7992381519',
            'driving_license': '123456789'
        }
        response = requests.post(BASE_URL_ENTITY + 'register/driver', json=data)
    return 

if __name__ == '__main__':
    test_monitoring()
    # driver_id,passenger_id =register()
    # main()

