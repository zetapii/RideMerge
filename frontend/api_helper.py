import requests
import json

# BASE_URL = 'http://0.0.0.0:5001'
BASE_URL = 'http://10.2.131.17:5005'
user_session = None


# Helper function to send requests to the backend
def send_request(endpoint, method='GET', data=None, base_url=None):
    if user_session:
        if data:
            data['token'] = user_session['token']

    if not base_url:
        base_url = BASE_URL

    url = f"{base_url}/{endpoint}"
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
