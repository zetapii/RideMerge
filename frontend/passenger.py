from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request, save_token


# Passenger Login and Registration
def passenger_login():
    layout = [[sg.Text('Passenger Login')],
              [LabelInputText(key='phone', prompt='Phone')],
              [
                  LabelInputText(key='password',
                                 password_char='*',
                                 prompt='Password')
              ], [sg.Button('Login'),
                  sg.Button('Register')]]

    window = sg.Window('Passenger Login', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Login':
            data = {'phone': values['phone'], 'password': values['password']}
            response = send_request('login/passenger', 'POST', data)
            if response['passenger_id']:
                sg.popup(
                    f"Login successful!\nPassenger ID: {response['passenger_id']}"
                )
                save_token(response['token'], 'passenger')
                switch_window(window, passenger_dashboard)
            else:
                sg.popup('Invalid credentials')
        elif event == 'Register':
            switch_window(window, register_passenger_window)

    window.close()


# Passenger Registration Window
def register_passenger_window():
    layout = [[sg.Text('Passenger Registration')],
              [LabelInputText(key='name', prompt='Name')],
              [LabelInputText(key='phone', prompt='Phone')],
              [LabelInputText(key='email', prompt='Email')],
              [
                  LabelInputText(key='password',
                                 password_char='*',
                                 prompt='Password')
              ], [sg.Button('Register'),
                  sg.Button('Cancel')]]

    window = sg.Window('Passenger Registration', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Register':
            data = {
                'name': values['name'],
                'phone': values['phone'],
                'email': values['email'],
                'password': values['password']
            }
            response = send_request('register/passenger', 'POST', data)
            if response['passenger_id']:
                sg.popup('Registration successful!')
                break
            else:
                sg.popup('Registration failed. Please try again.')

    window.close()


# Passenger Dashboard
def passenger_dashboard():
    layout = [[sg.Text('Book Ride')],
              LabelInputText('Start Location:', key='start_loc'),
              LabelInputText('End Location:', key='end_loc'),
              [sg.Checkbox('Is Secure Trip', key='is_secure_trip')],
              [sg.Button('Show Rides')],
              [sg.Listbox(values=[], key='rides', size=(50, 6))],
              [sg.Button('Book')], [sg.Button('Logout')]]

    window = sg.Window('Passenger Dashboard', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Logout'):
            break
        elif event == 'Show Rides':
            # Fetch rides from the backend
            response = send_request('fetch/vehicles', 'GET')
            if 'error' in response:
                sg.popup(response['error'])
            else:
                rides = response
                ride_data = {}
                for i, ride in enumerate(rides):
                    ride['estd_time_of_arrival'] = '10 mins'
                    ride['distance'] = '5 km'
                    ride['cost'] = 'Rs. 100'
                    ride_data[i] = {
                        'estd_time_of_arrival': ride['estd_time_of_arrival'],
                        'distance': ride['distance'],
                        'vehicle_model': ride['vehicle_model'],
                        'cost': ride['cost']
                    }
                window['rides'].update([
                    f"ETA: {ride['estd_time_of_arrival']}, Distance: {ride['distance']}, Car Model: {ride['vehicle_model']}, Cost: {ride['cost']}"
                    for ride in rides
                ])
        elif event == 'Book':
            selected_index = window['rides'].GetIndexes()[0]
            selected_ride = ride_data[selected_index]
            book_ride(values['start_loc'], values['end_loc'],
                      selected_ride['vehicle_model'], selected_ride['cost'])

    window.close()


# Book Ride Window
def book_ride(start_loc, end_loc, car_model, cost):
    layout = [[sg.Text('Confirm Ride')],
              [sg.Text(f'Start Location: {start_loc}')],
              [sg.Text(f'End Location: {end_loc}')],
              [sg.Text(f'Car Model: {car_model}')], [sg.Text(f'Cost: {cost}')],
              [sg.Button('Confirm'), sg.Button('Cancel')]]

    window = sg.Window('Book Ride', layout)

    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Confirm':
            sg.popup('Payment options will be implemented soon!')

    window.close()
