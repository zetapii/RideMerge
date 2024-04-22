#!/usr/bin/env python
import pika
import json

class SMSPublisher:
    def sendToAdmin(self,message = 'Monitoring Message -  ERROR BEING THROWN AT HIGH RATES'):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='SMSTopic')
        data = {
            'message': message,
            'receiver': 7992381519
        }
        json_data = json.dumps(data)

        channel.basic_publish(exchange='', routing_key='SMSTopic', body=json_data,properties=pika.BasicProperties(delivery_mode=2))
        connection.close()

    def sendToUser(self,email_id,message):

        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='SMSTopic')
        data = {
            'message': 'Ride Status Updated - Please Check',
            'receiver': 7992381519
        }
        json_data = json.dumps(data)

        channel.basic_publish(exchange='', routing_key='SMSTopic', body=json_data,properties=pika.BasicProperties(delivery_mode=2))
        connection.close()