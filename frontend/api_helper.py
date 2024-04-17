import requests
import json

# BASE_URL = 'http://0.0.0.0:5001'
BASE_URL = 'http://10.2.131.17:5001'
user_token = None


# Helper function to send requests to the backend
def send_request(endpoint, method='GET', data=None):
    if user_token:
        if data:
            data['token'] = user_token['token']

    url = f"{BASE_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if method == 'GET':
        response = requests.get(url)
    elif method == 'POST':
        response = requests.post(url, json=data, headers=headers)

    # debug log
    print(f"Request: {url}")
    print(f"Method: {method}")
    print(f"Data: {data}")
    print(f"Response: {response.text}")

    try:
        return response.json()
    except:
        return {'error': 'Server error'}


# Change BASE_URL
def change_base_url(new_base_url):
    global BASE_URL
    BASE_URL = new_base_url


# Save token to disk
def save_token(token, user_type):
    global user_token
    user_token = {'token': token, 'user_type': user_type}
    json.dump(user_token, open('token.json', 'w'))


# Load token from disk
def load_token():
    global user_token
    try:
        user_token = json.load(open('token.json', 'r'))
        return user_token
    except:
        return None
