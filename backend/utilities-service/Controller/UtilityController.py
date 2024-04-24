import sys
sys.path.append('../../utilities-service')

import json 
from enum import Enum
from flask import Flask, jsonify, request
import requests
from enum import IntEnum
from publishers import EmailPublisher,SMSPublisher

app = Flask(__name__)

@app.route('/notify_admin/error', methods=['POST'])
def notify_admin_error():
    try:
        # body = request.get_json()
        email_publisher = EmailPublisher.EmailPublisher()
        sms_publisher = SMSPublisher.SMSPublisher()

        email_publisher.sendToAdmin()
        sms_publisher.sendToAdmin()
        return jsonify({'status': 'message published'}), 200
    except Exception as e:
        return jsonify({'status': 'error in publishing', 'error': str(e)}), 500
        
@app.route('/notify_user/ride_status', methods=['POST'])
def notify_user_ride_status():
    try:
        body = request.get_json()
        phone_number = body.get('phone_number')
        email_id = body.get('email_id')
        message = body.get('message')
        email_publisher = EmailPublisher.EmailPublisher()
        sms_publisher = SMSPublisher.SMSPublisher()
        if phone_number:
            sms_publisher.sendToUser(phone_number,message)
        if email_id:
            email_publisher.sendToUser(email_id,message)
        return jsonify({'status': 'message published'}), 200
    except Exception as e:
        return jsonify({'status': 'error in publishing', 'error': str(e)}), 500
    
##write api to find the distance between two locations
@app.route('/fetch/distance', methods=['POST'])
def fetch_distance():
    try:
        body = request.get_json()
        source = body.get('source')
        destination = body.get('destination')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)