import requests
import json
from collections import defaultdict
from gui import sg

# BASE_URL = 'http://0.0.0.0:5001'
BASE_URL = 'http://10.2.131.17:5005'
user_session = None


# Helper function to send requests to the backend
def send_request(endpoint,
                 method='GET',
                 data=None,
                 base_url=None,
                 format='json'):
    if user_session:
        if data:
            data['token'] = user_session['token']

    if not base_url:
        base_url = BASE_URL

    url = f"{base_url}/{endpoint}"
    headers = {'Content-Type': 'application/json'}

    # debug log
    print(f"Request: {url}")
    print(f"Method: {method}")
    print(f"Data: {data}")

    try:
        if method == 'GET':
            if format == 'data':
                response = requests.get(url, data=data)
            else:
                response = requests.get(url)
        elif method == 'POST':
            if format == 'json':
                response = requests.post(url, json=data, headers=headers)
            else:
                response = requests.post(url, data=data, headers=headers)

        # debug log
        print(f"Response: {response.text}")

        # ensure KeyError is not raised
        if type(response.json()) == list:
            return response.json()
        # return defaultdict(lambda: None, response.json())
        # convert to defaultdict recursively
        return json.loads(json.dumps(response.json()), object_hook=lambda d: defaultdict(lambda: None, d))
    except Exception as e:
        error_json = {'error': 'Server error', 'debug': str(e)}
        print(error_json)
        return defaultdict(lambda: None, error_json)


# Change BASE_URL
def change_base_url(new_base_url):
    global BASE_URL
    BASE_URL = new_base_url


# Save token to disk
def save_session(token, user_type, user_id):
    global user_session
    user_session = {'token': token, 'user_type': user_type, 'user_id': user_id}
    json.dump(user_session, open(f'token_{user_type}.json', 'w'))


# Load session from disk
def load_session(user_type):
    global user_session
    try:
        user_session = json.load(open(f'token_{user_type}.json'))
        print("Existing session found")
        print(user_session)
        return user_session
    except:
        print("No existing session found")
        return None


# Clear session
def clear_session(user_type):
    global user_session
    user_session = None
    print("Session cleared")
    json.dump({}, open(f'token_{user_type}.json', 'w'))
