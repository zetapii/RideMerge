from gui import sg
from gui import LabelInputText, switch_window
from api_helper import send_request

# subscription_base_url = "http://10.2.131.17:5010"
subscription_base_url = "http://10.2.131.17:5005"


def payment_window():
    layout = [
        [sg.Text("Payment")],
        LabelInputText("Amount: ", key='amount'),
        LabelInputText("Card Number: ", key='card_number'),
        LabelInputText("Expiry Date: ", key='expiry_date'),
        LabelInputText("CVV: ", key='cvv'),
        [sg.Button('Pay')],
        [sg.Button('Back')],
    ]

    window = sg.Window("Payment", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break

    window.close()
    return 'paid'


def subscription_window(passenger_id):

    def make_column(plan, subscription_details=None):
        """
          {
            "_id": {
                "$oid": "6623ba738c90f0f79d1e9b16"
            },
            "apply_surge": "True",
            "discount_rate": 24.44,
            "premium_vehicle": "True",
            "price": 100.0,
            "safe_ride": "False"
        }
        """

        if subscription_details:
            if plan['_id']['$oid'] == subscription_details['benefit_id']:
                action_button = sg.Button('Cancel Subscription',
                                          button_color=('white', 'red'))
            else:
                action_button = sg.Button(
                    'Subscribe',
                    key=f"subscribe_{plan['_id']['$oid']}",
                    button_color=('white', 'green'),
                    disabled=True)
        else:
            action_button = sg.Button('Subscribe',
                                      key=f"subscribe_{plan['_id']['$oid']}",
                                      button_color=('white', 'green'))

        def bool_to_str(value):
            # tick symbol: ✓
            return '✓' if value else '✗'

        return sg.Column([
            # [sg.Text(f"Plan: {plan['_id']['$oid']}")],
            [sg.Text(f"Price: {plan['price']}")],
            [sg.Text(f"Discount Rate: {plan['discount_rate']}")],
            [
                sg.Text(
                    f"Premium Vehicle: {bool_to_str(plan['premium_vehicle'])}")
            ],
            [sg.Text(f"Safe Ride: {bool_to_str(plan['safe_ride'])}")],
            [sg.Text(f"Surge Benefit: {bool_to_str(not plan['apply_surge'])}")],
            [action_button],
        ])

    response = send_request('get_benefit', 'GET', format='data')
    plans = response['benefits']
    response = send_request(f'find_subscription',
                            'GET', {'userid': passenger_id},
                            format='data')
    #  {"message": "Not Found"}
    if response['message'] == 'Not Found':
        subscription_details = None
    else:
        subscription_details = response['subscription_details']
        print("Hurrah", subscription_details)

    plan_columns = []
    for plan in plans:
        plan_columns.append(make_column(plan, subscription_details))

    if subscription_details:
        import time
        """2024-04-22 00:00:00"""
        start_date = time.mktime(
            time.strptime(subscription_details['start_date'],
                          "%Y-%m-%d %H:%M:%S"))
        expiry_date = time.mktime(
            time.strptime(subscription_details['expiry_date'],
                          "%Y-%m-%d %H:%M:%S"))
        now = time.time()
        progress = int((now - start_date) / (expiry_date - start_date) * 100)
        days_left = int((expiry_date - now) / (60 * 60 * 24))
        subscription_layout = [
            [sg.Text("Current Subscription")],
            [sg.Text(f'Start date: {subscription_details["start_date"]}')],
            [sg.Text(f'Expiry date: {subscription_details["expiry_date"]}')],
            # [sg.Text(f'Duration: {subscription_details["duration"]} days')],
            # [sg.Text(f'Benefit ID: {subscription_details["benefit_id"]}')],
            [
                sg.Text(f'Days left: {days_left}'),
                sg.ProgressBar(100,
                               key='ProgressBar',
                               size=(20, 20),
                               expand_x=True,
                               border_width=1,
                               relief='solid')
            ],
        ]
    else:
        subscription_layout = [
            [sg.Text("No Subscription")],
        ]

    layout = [[sg.Text("Subscription Plans")], subscription_layout,
              plan_columns,
              [
                  sg.Text("Duration"),
                  sg.Radio('1 month', 'duration', key='30', default=True),
                  sg.Radio('3 months', 'duration', key='90'),
                  sg.Radio('6 months', 'duration', key='180'),
                  sg.Radio('1 year', 'duration', key='365'),
              ], [sg.Button('Renew')], [
                  sg.Button('Back'),
              ]]

    def get_duration(values):
        duration = 30
        for key in values:
            if values[key]:
                duration = int(key)
                break
        return duration

    window = sg.Window("Subscription", layout, finalize=True)
    # import pywinstyles
    # pywinstyles.apply_style(window, 'mica')

    # update progress bar
    if subscription_details:
        window['ProgressBar'].update_bar(progress)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        elif event.startswith('subscribe'):
            plan_id = event.split('_')[1]
            response = send_request('add',
                                    'GET', {
                                        'userid': passenger_id,
                                        'benefit_id': plan_id,
                                        'duration': get_duration(values),
                                    },
                                    base_url=subscription_base_url,
                                    format='data')

            if response['message'] == 'SubscriptionAlreadyExists':
                sg.popup('Subscription already exists')
            elif response['message'] == 'OK':
                subscription_id = response['subscription_id']
                sg.popup('Subscription added')
        elif event == 'Cancel Subscription':
            response = send_request('delete',
                                    'GET', {
                                        'userid': passenger_id,
                                    },
                                    base_url=subscription_base_url,
                                    format='data')
            if response['message'] == 'OK':
                sg.popup('Subscription cancelled')
            else:
                sg.popup('Failed to cancel subscription')
        elif event == 'Renew':
            response = send_request('renew_subscription',
                                    'GET', {
                                        'userid': passenger_id,
                                        'new_duration': get_duration(values),
                                    },
                                    base_url=subscription_base_url,
                                    format='data')
            if response['message'] == 'OK':
                sg.popup('Subscription renewed')
            else:
                sg.popup('Failed to renew subscription')

    window.close()
