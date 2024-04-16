from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request, save_token


# Driver Login Window
def driver_login():
    layout = [[sg.Text('Driver Login')],
              [LabelInputText(key='phone', prompt='Phone')],
              [
                  LabelInputText(key='password',
                                 password_char='*',
                                 prompt='Password')
              ], [sg.Button('Login'),
                  sg.Button('Register')]]

    window = sg.Window('Driver Login', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Login':
            data = {'phone': values['phone'], 'password': values['password']}
            response = send_request('login/driver', 'POST', data)
            if response['driver_id']:
                sg.popup(
                    f"Login successful!\nDriver ID: {response['driver_id']}")
                save_token(response['token'], 'driver')
                switch_window(window,
                              lambda: driver_dashboard(response['driver_id']))
            else:
                sg.popup('Invalid credentials')
        elif event == 'Register':
            switch_window(window, register_driver_window)

    window.close()


# Driver Registration Window
def register_driver_window():
    layout = [
        [sg.Text('Driver Registration')],
        [LabelInputText(key='name', prompt='Name')],
        [LabelInputText(key='phone', prompt='Phone')],
        [LabelInputText(key='email', prompt='Email')],
        [LabelInputText(key='password', password_char='*', prompt='Password')],
        [LabelInputText(key='driving_license', prompt='Driving License')],
        [sg.Button('Register'), sg.Button('Cancel')]
    ]

    window = sg.Window('Driver Registration', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Register':
            data = {
                'name': values['name'],
                'phone': values['phone'],
                'email': values['email'],
                'password': values['password'],
                'driving_license': values['driving_license']
            }
            response = send_request('register/driver', 'POST', data)
            if response['driver_id']:
                sg.popup('Registration successful!')
                break
            else:
                sg.popup('Registration failed. Please try again.')

    window.close()


# Add Vehicle Window
def add_vehicle_window(driver_id):
    layout = [[sg.Text('Add Vehicle')],
              LabelInputText('Vehicle Model:', key='vehicle_model'),
              LabelInputText('Registration Number:',
                             key='registration_number'),
              LabelInputText('Insurance Number:', key='insurance_number'),
              LabelInputText('Manufacturer:', key='manufacturer'),
              LabelInputText('Manufacturing Year:', key='manufacturing_year'),
              [sg.Button('Add Vehicle'),
               sg.Button('Cancel')]]

    window = sg.Window('Add Vehicle', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Add Vehicle':
            data = {
                'driver_id': driver_id,
                'vehicle_model': values['vehicle_model'],
                'registration_number': values['registration_number'],
                'insurance_number': values['insurance_number'],
                'manufacturer': values['manufacturer'],
                'manufacturing_year': values['manufacturing_year']
            }
            response = send_request('driver/add_vehicle', 'POST', data)
            # TODO
            # if response['status']:
            if response['vehicle_id']:
                sg.popup('Vehicle added successfully!')
                break
            else:
                sg.popup('Vehicle addition failed. Please try again.')
    window.close()


# Show My Vehicles Window
def show_my_vehicles(driver_id):
    layout = [[sg.Text('My Vehicles')],
              [sg.Listbox(values=[], key='vehicles', size=(50, 6))],
              [sg.Button('Refresh'), sg.Button('Close')]]

    window = sg.Window('My Vehicles', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event == 'Refresh':
            # TODO
            # response = send_request(f'fetch/vehicles/{driver_id}', 'GET')
            response = send_request(f'fetch/vehicles', 'GET')
            if 'error' in response:
                sg.popup(response['error'])
            else:
                vehicles = response
                window['vehicles'].update([
                    f"Vehicle ID: {vehicle['id']}, Model: {vehicle['vehicle_model']}, Registration: {vehicle['registration_number']}"
                    for vehicle in vehicles
                ])

    window.close()


# Driver Dashboard
def driver_dashboard(driver_id):
    layout = [[sg.Text(f"Driver ID: {driver_id}")],
              [sg.Button('Rides Available')], [sg.Text('Set Vehicle Status')],
              [
                  sg.Radio('Offline', 'status', key='offline', default=True),
                  sg.Radio('Riding', 'status', key='riding'),
                  sg.Radio('Available', 'status', key='available')
              ], [sg.Button('Update Status')], [sg.Button('Add Vehicle')],
              [sg.Button('My Vehicles')], [sg.Button('Logout')]]

    window = sg.Window('Driver Dashboard', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Logout'):
            break
        elif event == 'Update Status':
            status = next((k for k, v in values.items() if v), None)
            data = {'driver_id': driver_id, 'status': status}
            response = send_request('driver/update_status', 'POST', data)
            if response['status']:
                sg.popup('Status updated successfully!')
        elif event == 'Add Vehicle':
            switch_window(window, lambda: add_vehicle_window(driver_id))
        elif event == 'My Vehicles':
            switch_window(window, lambda: show_my_vehicles(driver_id))

    window.close()
