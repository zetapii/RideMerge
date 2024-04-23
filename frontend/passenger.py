from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request, clear_session
from subscription import subscription_window
from MapWidget import MapWidget
import textwrap


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
def passenger_dashboard(passenger_id):
    # # check if a ride exists
    # response = send_request(f'passenger/current_ride/{passenger_id}', 'GET')

    # # NOTE: if we get 'ride_id' field, it means we have an existing ride
    # if response['ride_id']:
    #     # TODO: fare is not available in the response
    #     ride_status_window(response['ride_id'], response['start_location'],
    #                        response['drop_location'],
    #                        response['vehicle_model'], 100)

    # map things ===============================================
    map_widget = MapWidget('map_canvas')
    source_ll = None
    dest_ll = None
    # =========================================================

    layout = [
        [sg.Text('Book Ride', justification='center', expand_x=True)],
        [sg.Text('', key='start_loc')],
        [sg.Text('', key='end_loc')],
        [
            sg.Column([
                [sg.Text('Choose Start and End location:')],
                [sg.Checkbox('Is Secure Trip', key='is_secure_trip')],
                map_widget.element,
            ]),
            sg.Column([
                [sg.Button('Show Rides')],
                [sg.Listbox(values=[], key='rides', size=(30, 10))],
            ]),
            sg.Column([
                [sg.Button('Book')],
                [sg.Button('Ride History')],
                [sg.Button('View Subscriptions')],
                [sg.Button('Logout')],
            ]),
        ],
    ]

    window = sg.Window('Passenger Dashboard',
                       layout,
                       finalize=True,
                       return_keyboard_events=True)

    # initialize map
    map_widget.setup()

    ride_data = {}

    def show_rides_click():
        # Fetch rides from the backend
        response = send_request(
            'passenger/rides',
            'POST',
            {
                'passenger_id': passenger_id,
                # 'source': values['start_loc'],
                # 'destination': values['end_loc'],
                'source': source_ll,
                'destination': dest_ll,
                'is_secure': values['is_secure_trip']
            })
        if 'error' in response:
            sg.popup(response['error'])
        else:
            rides = response
            ride_data.clear()
            for i, ride in enumerate(rides):
                ride_data[i] = {
                    'vehicle_model': ride['model'],
                    'fare': ride['fare']
                }
            window['rides'].update([
                f"Vehicle: {ride['model']} | Fare: {ride['fare']}"
                for ride in rides
            ])

    def book_ride_click():
        selected_index = window['rides'].GetIndexes()[0]
        selected_ride = ride_data[selected_index]

        # Book the selected ride
        response = send_request(
            'passenger/book_ride',
            'POST',
            {
                'passenger_id': passenger_id,
                'vehicle_model': selected_ride['vehicle_model'],
                # 'source': values['start_loc'],
                # 'destination': values['end_loc'],
                'source': source_ll,
                'destination': dest_ll,
                'is_secure': values['is_secure_trip'],
            })

        if response['ride_id']:
            switch_window(
                window,
                lambda: ride_status_window(response['ride_id'], values[
                    'start_loc'], values['end_loc'], selected_ride[
                        'vehicle_model'], selected_ride['fare']))
        else:
            sg.popup('Ride booking failed. Please try again.')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Show Rides':
            if source_ll is None or dest_ll is None:
                sg.popup('Please select start and end locations')
                continue
            show_rides_click()
        elif event == 'Book':
            # check if a ride is selected
            if not window['rides'].GetIndexes():
                sg.popup('Please select a ride')
                continue
            book_ride_click()
        elif event == 'Ride History':
            switch_window(window, lambda: ride_history_window(passenger_id))
        elif event == 'View Subscriptions':
            switch_window(window, lambda: subscription_window(passenger_id))
        elif event == 'Logout':
            clear_session(user_type='passenger')
            break
        map_event = map_widget.handle_event(event, values)

        def update_direction():
            if source_ll and dest_ll:
                map_widget.update_direction('from', 'to',
                                            map_widget.get_directions())

        if map_event == 'location_from_set':
            new_text = "Pickup: " + map_widget.get_address(
                map_widget.location_from)
            new_text = textwrap.fill(new_text, width=80)
            window['start_loc'].update(new_text)
            source_ll = ",".join(map(str, map_widget.location_from))
            update_direction()

        elif map_event == 'location_to_set':
            new_text = "Drop: " + map_widget.get_address(
                map_widget.location_to)
            new_text = textwrap.fill(new_text, width=80)
            window['end_loc'].update(new_text)
            dest_ll = ",".join(map(str, map_widget.location_to))
            update_direction()

    window.close()


# Ride History Window
def ride_history_window(passenger_id):
    layout = [
        [sg.Text('Ride History')],
        [sg.Text('Select a ride to view details')],
        [sg.Listbox(values=[], key='rides', size=(50, 6))],
        # [sg.Button('View Details')],
        [sg.Button('Back')],
    ]

    window = sg.Window('Ride History', layout, finalize=True)

    # fetch history from the backend
    response = send_request(f'passenger/ride_history/{passenger_id}', 'GET')
    rides = response

    ride_data = {}
    for i, ride in enumerate(rides):
        ride_data[i] = {
            'start_loc': ride['start_location'],
            'end_loc': ride['drop_location'],
            'vehicle_model': ride['vehicle_model'],
            'status': ride['status'],
        }

    window['rides'].update([
        f"Start: {ride['start_location']} | Drop: {ride['drop_location']} | Vehicle: {ride['vehicle_model']} | Status: {ride['status']}"
        for ride in rides
    ])

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break

    window.close()


# Payment Window
def payment_window(ride_id, amount, user_id, driver_id):
    layout = [
        [sg.Text('Payment')],
        [LabelInputText('UPI ID:', key='upi_id')],
        [LabelInputText('PIN:', key='pin', password_char='*')],
        [sg.Button('Pay')],
    ]

    window = sg.Window('Payment', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Pay':
            data = {
                'user_id': user_id,
                'ride_id': ride_id,
                'driver_id': driver_id,
                'upi_id': values['upi_id'],
                'pin': values['pin'],
                'amount': amount
            }
            # response = send_request('payment/upi', 'POST', data)
            response = {'status': 'success'}
            if response['status'] == 'success':
                sg.popup('Payment successful!')
                break
            else:
                sg.popup('Payment failed. Please try again.')

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

    # TODO: implement payment gateway integration here
    switch_window(window, lambda: payment_window(ride_id, fare, 1, 1))

    window.close()


# Ride Status Window
def ride_status_window(ride_id, start_loc, end_loc, vehicle_model, fare):
    layout = [
        [
            sg.Text('Waiting for driver to accept the ride...',
                    key='status_msg')
        ],
        [sg.Text(f'Start Location: {start_loc}')],
        [sg.Text(f'End Location: {end_loc}')],
        [sg.Text(f'Vehicle Model: {vehicle_model}')],
        [sg.Text(f'Fare: {fare}')],
        [sg.Text(f'Driver:'), sg.Text('-', key='driver')],
        [sg.Text(f'Ride ID: {ride_id}')],
        [sg.Text(f'Ride Status:'),
         sg.Text('-', key='status')],
        [sg.Text(f'Ride OTP:'), sg.Text('-', key='otp')],
        [sg.Button('Refresh'), sg.Button('Cancel Ride')],
    ]

    window = sg.Window('Book Ride', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Refresh':
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
            window['otp'].update(response['ride_otp'])
            window['driver'].update(response['driver_id'])
            window['status_msg'].update(status_msgs[response['status']])

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
                        ride_id, start_loc, end_loc, vehicle_model, fare))
                break
        elif event == 'Cancel Ride':
            response = send_request(f'passenger/cancel_ride', 'POST',
                                    {'ride_id': ride_id})
            if response['status'] == 'success':
                sg.popup('Ride cancelled successfully!')
                break
            else:
                sg.popup('Ride cancellation failed. Please try again.')

    window.close()
