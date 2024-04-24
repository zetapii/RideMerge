from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request, clear_session, BASE_URL

payment_base_url = 'http://10.2.136.139:5014'

# payment_base_url = BASE_URL


# Wallet Window
def wallet_window(driver_id):
    layout = [
        [sg.Text('Wallet')],
        [sg.Text('Balance:'), sg.Text('', key='balance')],
        [sg.Button('Payment History')],
        [sg.Button('Refresh')],
        [sg.Button('Close')],
    ]

    window = sg.Window('Wallet', layout)

    while True:
        event, values = window.read(timeout=5000)
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in ('Refresh', sg.TIMEOUT_EVENT):
            response = send_request(f'wallet_amount/{driver_id}',
                                    'GET',
                                    base_url=payment_base_url)
            if response['data']:
                window['balance'].update(response['data'])
        elif event == 'Payment History':
            switch_window(window,
                          lambda: payment_history_window(driver_id, 'driver'))

    window.close()


def payment_history_window(user_id, user_type):
    if user_type == 'passenger':
        api_url = f'user_history/{user_id}'
        headings = [
            'ride_id', 'driver_id', 'amount', 'payment_method',
            'date', 'status'
        ]
    else:
        api_url = f'wallet_history/{user_id}'
        headings = [
            'user_id', 'ride_id', 'amount', 'payment_method',
            'date', 'status'
        ]
    response = send_request(api_url, 'GET', base_url=payment_base_url)
    payment_history = response['data']

    if not payment_history:
        sg.popup('No payment history found.')
        return

    layout_payment_history = [[
        sg.Table(values=payment_history,
                 headings=headings,
                 key='Table',
                 auto_size_columns=False,
                 justification='center')
    ], [sg.Button('Refresh'), sg.Button('Back')]]

    layout = [[
        sg.TabGroup([[sg.Tab('Payment History', layout_payment_history)]])
    ]]

    window = sg.Window('Payment History', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Refresh':
            response = send_request(api_url, 'GET', base_url=payment_base_url)
            payment_history = response['data']

            if not payment_history:
                continue

            # window['payment_history'].update(payment_history_csv)
            window['Table'].update(values=payment_history)

        if event == 'Back':
            switch_window(window, 'payment_history')

    window.close()


def payment_window(ride_id, amount, passenger_id, driver_id):
    layout_credit_card = [
        [sg.Text('Amount'), sg.Text(amount, key='amount')],
        LabelInputText('Card Number', key='card_number'),
        LabelInputText('Expiration Date', key='expiration_date'),
        LabelInputText('CVV', key='cvv'),
        [sg.Button('Pay', key='pay_credit_card')],
    ]

    layout_debit_card = [
        [sg.Text('Amount'), sg.Text(amount, key='amount')],
        LabelInputText('Card Number', key='card_number'),
        LabelInputText('Expiration Date', key='expiration_date'),
        LabelInputText('CVV', key='cvv'),
        [sg.Button('Pay', key='pay_debit_card')],
    ]

    layout_upi = [
        [sg.Text('Amount'), sg.Text(amount, key='amount')],
        LabelInputText('UPI ID', key='upi_id'),
        LabelInputText('PIN', key='pin', password_char='*'),
        [sg.Button('Pay', key='pay_upi')],
    ]

    layout = [
        [
            sg.TabGroup([[sg.Tab('Credit Card', layout_credit_card)],
                         [sg.Tab('Debit Card', layout_debit_card)],
                         [sg.Tab('UPI', layout_upi)]])
        ],
        [sg.Button('View Payment History'),
         sg.Button('Back')],
    ]

    window = sg.Window('Payment', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'pay_credit_card':
            data = {
                'user_id': passenger_id,
                'ride_id': ride_id,
                'driver_id': driver_id,
                'card_number': values['card_number'],
                'expiration_date': values['expiration_date'],
                'cvv': values['cvv'],
                'amount': amount
            }
            response = send_request('creditcard',
                                    'POST',
                                    data,
                                    base_url=payment_base_url)

            if response['status'] == 'success':
                sg.popup('Payment successful!')
            else:
                sg.popup('Payment failed. Please try again.')

        elif event == 'pay_debit_card':
            data = {
                'user_id': passenger_id,
                'ride_id': ride_id,
                'driver_id': driver_id,
                'card_number': values['card_number'],
                'expiration_date': values['expiration_date'],
                'cvv': values['cvv'],
                'amount': amount
            }
            response = send_request('debitcard',
                                    'POST',
                                    data,
                                    base_url=payment_base_url)

            if response['status'] == 'success':
                sg.popup('Payment successful!')
            else:
                sg.popup('Payment failed. Please try again.')

        elif event == 'pay_upi':
            data = {
                'user_id': passenger_id,
                'ride_id': ride_id,
                'driver_id': driver_id,
                'upi_id': values['upi_id'],
                'pin': values['pin'],
                'amount': amount
            }
            response = send_request('upi',
                                    'POST',
                                    data,
                                    base_url=payment_base_url)

            if response['status'] == 'success':
                sg.popup('Payment successful!')
            else:
                sg.popup('Payment failed. Please try again.')

        if event == 'View Payment History':
            switch_window(window, lambda: payment_history_window(passenger_id))

    window.close()
