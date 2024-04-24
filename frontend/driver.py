from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request, clear_session
from payment import payment_history_window,wallet_window
import textwrap

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
def my_vehicles_window(driver_id):
    layout = [[sg.Text('My Vehicles')],
              [sg.Listbox(values=[], key='vehicles', size=(50, 6))],
              [sg.Text('Set Vehicle Status')],
              [
                  sg.Radio('Offline', 'status', key='OFFLINE', default=True),
                  sg.Radio('Available', 'status', key='WAITING'),
              ], [sg.Button('Update Status')],
              [sg.Button('Refresh'), sg.Button('Close')]]

    window = sg.Window('My Vehicles', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event == 'Refresh':
            # TODO
            response = send_request(f'fetch/driver_vehicles/{driver_id}',
                                    'GET')
            if response:
                vehicles = response
                vehicle_data = {}
                for i, vehicle in enumerate(vehicles):
                    vehicle_data[i] = {
                        'driver_vehicle_id': vehicle['id'],
                        'driver_id': vehicle['driver_id'],
                        'vehicle_id': vehicle['vehicle_id'],
                        'model': vehicle['model'],
                        'status': vehicle['status'],
                        'current_location': vehicle['current_location'],
                        'registration_number': vehicle['registration_number'],
                    }
                window['vehicles'].update([
                    f"Model: {vehicle['model']} | Status: {vehicle['status']} | Location: {vehicle['current_location']}"
                    for vehicle in vehicles
                ])
        elif event == 'Update Status':
            status = 'OFFLINE' if values['OFFLINE'] else 'WAITING'

            if not window['vehicles'].GetIndexes():
                sg.popup('Please select a vehicle to update status')
                continue

            # get selected vehicle
            selected_index = window['vehicles'].GetIndexes()[0]
            selected_vehicle = vehicle_data[selected_index]

            data = {
                'driver_vehicleid': selected_vehicle['driver_vehicle_id'],
                'status': status
            }
            response = send_request('driver/change_status', 'POST', data)
            if response['status'] == 'success':
                sg.popup('Status updated successfully!')
            else:
                sg.popup('Status update failed. Please try again.')

    window.close()


# Rides Available Window
def rides_available_window(driver_id):
    layout = [
        [sg.Text('Rides Available')],
        [sg.Text('Select a ride to accept')],
        [sg.Listbox(values=[], key='rides', size=(50, 6))],
        [sg.Button('Accept')],
        [sg.Button('Refresh'), sg.Button('Close')],
    ]

    window = sg.Window('Rides Available', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event == 'Refresh':
            response = send_request(f'driver/rides/{driver_id}', 'GET')
            if 'error' in response:
                sg.popup(response['error'])
            else:
                rides = response
                ride_data = {}
                for i, ride in enumerate(rides):
                    ride_data[i] = {
                        'ride_id': ride['ride_id'],
                        'passenger_name': ride['passenger_name'],
                        'start_location': ride['start_location'],
                        'drop_location': ride['drop_location'],
                        'start_address': ride['start_address'],
                        'drop_address': ride['drop_address'],
                    }
                window['rides'].update([
                    f"Passenger: {ride['passenger_name']} | Start: {ride['start_address']} | Drop: {ride['drop_address']}"
                    for ride in rides
                ])
        elif event == 'Accept':
            if not window['rides'].GetIndexes():
                sg.popup('Please select a ride to accept')
                continue

            selected_index = window['rides'].GetIndexes()[0]
            selected_ride = ride_data[selected_index]
            data = {
                'driver_id': driver_id,
                'ride_id': selected_ride['ride_id']
            }
            response = send_request('driver/accept_ride', 'POST', data)
            if response['status'] == 'success':
                sg.popup('Ride accepted successfully!')
                switch_window(
                    window, lambda: ride_status_window(
                        selected_ride['ride_id'], selected_ride[
                            'start_location'], selected_ride['drop_location'],
                        selected_ride['start_address'], selected_ride[
                            'drop_address'], None, None))
            else:
                sg.popup('Ride acceptance failed. Please try again.')

    window.close()

# Driver Dashboard
def driver_dashboard(driver_id):
    # check if a ride exists
    response = send_request(f'driver/current_ride/{driver_id}', 'GET')

    # NOTE: if we get 'ride_id' field, it means we have an existing ride
    if response['ride_id']:
        # TODO: fare is not available in the response
        ride_status_window(response['ride_id'], response['start_location'],
                           response['drop_location'],
                           response['start_address'], response['drop_address'],
                           response['vehicle_model'], 100)

    # fetch driver name
    response = send_request(f'fetch/driver/{driver_id}', 'GET')
    driver_name = response['name']

    layout = [
        [sg.Text(f"Driver Name: {driver_name}")],
        [sg.Button('Rides Available')],
        [sg.Button('Add Vehicle')],
        [sg.Button('My Vehicles')],
        [sg.Button('Wallet')],
        [sg.Button('Logout')],
    ]

    window = sg.Window('Driver Dashboard', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Add Vehicle':
            switch_window(window, lambda: add_vehicle_window(driver_id))
        elif event == 'My Vehicles':
            switch_window(window, lambda: my_vehicles_window(driver_id))
        elif event == 'Rides Available':
            switch_window(window, lambda: rides_available_window(driver_id))
        elif event == 'Wallet':
            switch_window(window, lambda: wallet_window(driver_id))
        elif event == 'Logout':
            clear_session(user_type='driver')
            break

    window.close()


# Ride completed window
def ride_completed_window(ride_id, start_loc, end_loc, vehicle_model, fare):
    layout = [
        [sg.Text('Ride Completed!')],
        [sg.Text(f'Start Location: {start_loc}')],
        [sg.Text(f'End Location: {end_loc}')],
        [sg.Text(f'Vehicle Model: {vehicle_model}')],
        [sg.Text(f'Fare: {fare}')],
        [sg.Button('Close')],
    ]

    window = sg.Window('Ride Completed', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break

    window.close()


# Ride Status Window
def ride_status_window(ride_id, start_loc, end_loc, start_address, end_address,
                       vehicle_model, fare):

    # wrap address
    start_address = textwrap.fill(start_address, width=50)
    end_address = textwrap.fill(end_address, width=50)

    layout = [
        [sg.Text('...', key='status_msg')],
        [sg.Text(f'Start Location: {start_address}')],
        [sg.Text(f'End Location: {end_address}')],
        [sg.Text(f'Vehicle Model: {vehicle_model}')],
        [sg.Text(f'Fare: {fare}', key='fare_label')],
        [sg.Text(f'Passenger:'),
         sg.Text('-', key='passenger')],
        [sg.Text(f'Ride ID: {ride_id}')],
        [sg.Text(f'Ride Status:'),
         sg.Text('-', key='status')],
        [
            LabelInputText('Enter OTP:', key='otp'),
            sg.Button('Submit', key='otp_submit')
        ],
        [
            sg.Button('Complete Ride'),
        ],
        [sg.Button('Refresh'), sg.Button('Cancel Ride')],
    ]

    window = sg.Window('Book Ride', layout, finalize=True)

    while True:
        event, values = window.read(timeout=5000)
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event in ('Refresh', sg.TIMEOUT_EVENT):
            # Fetch ride status from the backend
            response = send_request(f'ride_details/{ride_id}', 'GET')

            old_status = window['status'].DisplayText

            # update layout
            status_msgs = {
                'PENDING': 'Waiting for driver to accept the ride...',
                'ACCEPTED': 'Driver accepted the ride!',
                'PASSENGER_PICKED': 'Driver is on the way to pick you up!',
                'DRIVER_CANCELLED': 'Driver cancelled the ride',
                'PASSENGER_CANCELLED': 'You cancelled the ride',
                'COMPLETED': 'Ride completed!',
            }
            if old_status != response['status']:
                sg.popup(status_msgs[response['status']])

            window['status'].update(response['status'])
            window['passenger'].update(response['passenger_name'])
            window['status_msg'].update(status_msgs[response['status']])
            window['fare_label'].update(f'Fare: {response["fare"]}')

            if response['status'] == 'PENDING':
                pass
            elif response['status'] == 'ACCEPTED':
                pass
            elif response['status'] == 'PASSENGER_PICKED':
                pass
            elif response['status'] == 'DRIVER_CANCELLED':
                break
            elif response['status'] == 'PASSENGER_CANCELLED':
                break
            elif response['status'] == 'COMPLETED':
                switch_window(
                    window, lambda: ride_completed_window(
                        ride_id, start_address, end_address, vehicle_model, fare))
                break
        elif event == 'otp_submit':
            data = {'ride_id': ride_id, 'otp': values['otp']}
            response = send_request('driver/pickup_passenger', 'POST', data)
            if response['status'] == 'success':
                sg.popup('Passenger picked up successfully!')
                # disable the OTP field
                window['otp'].update(disabled=True)
            else:
                sg.popup('Passenger pickup failed. Please try again.')
        elif event == 'Complete Ride':
            response = send_request('driver/complete_ride', 'POST',
                                    {'ride_id': ride_id})
            if response['status'] == 'success':
                sg.popup('Ride completed successfully!')
                switch_window(
                    window, lambda: ride_completed_window(
                        ride_id, start_loc, end_loc, vehicle_model, fare))
                break
            else:
                sg.popup('Ride completion failed. Please try again.')
        elif event == 'Cancel Ride':
            response = send_request(f'passenger/cancel_ride', 'POST',
                                    {'ride_id': ride_id})
            if response['status'] == 'success':
                sg.popup('Ride cancelled successfully!')
                break
            else:
                sg.popup('Ride cancellation failed. Please try again.')

    window.close()
