from gui import sg
from gui import switch_window
from api_helper import send_request, change_base_url, BASE_URL, load_token
from passenger import passenger_login
from driver import driver_login


# Main Menu
def main_menu():
    layout = [
        [sg.Text('User/Driver Login Option')],
        [sg.Button('Driver Login'),
         sg.Button('Passenger Login')],
        [sg.HorizontalSeparator()],
        [
            sg.Text('API Base URL:', size=(20, 1)),
            sg.InputText(key='base_url', default_text=BASE_URL, expand_x=True)
        ],
        [sg.Button('Update URL'), sg.Button('Ping')],
    ]

    window = sg.Window('Main Menu', layout)

    # check for existing session token
    token = load_token()
    if token:
        # TODO
        event, values = window.read()
        if token['user_type'] == 'driver':
            switch_window(window, driver_login)
        elif token['user_type'] == 'passenger':
            switch_window(window, passenger_login)
    else:
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Driver Login':
                switch_window(window, driver_login)
            elif event == 'Passenger Login':
                switch_window(window, passenger_login)
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


if __name__ == '__main__':
    main_menu()
