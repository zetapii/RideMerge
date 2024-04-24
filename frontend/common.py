from gui import sg
from gui import switch_window, LabelInputText
from api_helper import send_request, change_base_url, BASE_URL, load_session, save_session
from passenger import passenger_dashboard, register_passenger_window
from driver import driver_dashboard, register_driver_window


# Driver and Passenger Login Function
def login_window(user_type):
    user_type_human = user_type.capitalize()

    layout = [
        [sg.Text(f'{user_type_human} Login')],
        [LabelInputText(key='phone', prompt='Phone')],
        [LabelInputText(key='password', password_char='*', prompt='Password')],
        [sg.Button('Login'), sg.Button('Cancel')],
    ]

    window = sg.Window(f'{user_type_human} Login', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Login':
            data = {'phone': values['phone'], 'password': values['password']}
            endpoint = f'login/{user_type}'
            response = send_request(endpoint, 'POST', data)
            user_id = response[f'{user_type}_id']
            if user_id:
                sg.popup(f"Login successful!\n{user_type} ID: {user_id}")
                save_session(response['token'], user_type, user_id)
                if user_type == 'driver':
                    switch_window(window, lambda: driver_dashboard(user_id))
                elif user_type == 'passenger':
                    switch_window(window, lambda: passenger_dashboard(user_id))
            else:
                sg.popup('Invalid credentials')

    window.close()


# Main Menu
def main_menu(user_type):
    # check for existing session
    session = load_session(user_type=user_type)
    if session:
        if session['user_type'] == 'driver':
            driver_dashboard(session['user_id'])
        elif session['user_type'] == 'passenger':
            passenger_dashboard(session['user_id'])
        return

    user_type_human = user_type.capitalize()

    layout = [
        [
            sg.Text(f'{user_type_human} Login'),
            sg.Button('Login'),
            sg.Button(f'Register New {user_type_human}')
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Text('API Base URL:', size=(20, 1)),
            sg.InputText(key='base_url', default_text=BASE_URL, expand_x=True)
        ],
        [sg.Button('Update URL'), sg.Button('Ping')],
    ]
    window = sg.Window(f'Main Menu: {user_type_human}', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Login':
            switch_window(window, lambda: login_window(user_type=user_type))
        elif event == 'Register New Passenger':
            switch_window(window, register_passenger_window)
        elif event == 'Register New Driver':
            switch_window(window, register_driver_window)
        elif event == 'Update URL':
            change_base_url(values['base_url'])
        elif event == 'Ping':
            response = send_request('/ping', 'GET')
            if 'status' not in response:
                sg.popup('Server is offline!')
            else:
                if response['status'] == 'pong':
                    sg.popup('Server is online!')
                else:
                    sg.popup('Server is offline!')
    window.close()
