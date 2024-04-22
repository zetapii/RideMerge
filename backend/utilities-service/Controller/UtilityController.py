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
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
