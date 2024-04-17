import requests


def register():
    
    ##write code to test above 3 apis 
    BASE_URL = "http://127.0.0.1:5001/"
    data = {
        'name': 'driver1',
        'password': 'driver1',
        'email': 'driver1',
        'phone' :'7992381519',
        'driving_license': '123456789'
    }
    response1 = requests.post(BASE_URL + 'register/driver', json=data)
    print(response1.json())
    data = {
        'name': 'passenger1',
        'password': 'passenger1',
        'email': 'passenger1',
        'phone' :'9198776090',
    }
    response = requests.post(BASE_URL + 'register/passenger', json=data)
    print(response.json())

    data = {
        'driver_id': response1.json()['driver_id'],
        'vehicle_model': 'swift',
        'registration_number': '123',
        'insurance_number': '123',
        'manufacturer': '123',
        'manufacturing_year': '123'
    }
    response = requests.post(BASE_URL + 'driver/add_vehicle', json=data)
    print(response.json())
        


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

if __name__ == '__main__':
    register()
    # main()

