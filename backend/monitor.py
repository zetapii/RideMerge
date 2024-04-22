import sys
sys.path.append('../../rides-service')

import redis
import time
import requests

redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

THRESHOLD_ERRORS = 20

UTILITY_SERVICE_URL = 'http://localhost:5008/'

def invalidate_redis_keys(keys):
    try:
        redis_client.delete(*keys)
    except redis.RedisError as e:
        print(f"Redis Error: {e}")

def check_error_count():
    try:
        cnt_errors = redis_client.get('cnt_errors')
        if cnt_errors and int(cnt_errors) > THRESHOLD_ERRORS:
            redis_client.set('cnt_errors', 0)
            return True
        return False
    except redis.RedisError as e:
        print(f"Redis Error: {e}")
        return False

def main():
    while True:
        if check_error_count():
            print("Error threshold reached. Notifying admin...")
            response = requests.post(UTILITY_SERVICE_URL + 'notify_admin/error')
            if response.status_code == 200:
                print("Admin notified.")
            else:
                print("Error notifying admin.")
        time.sleep(60)