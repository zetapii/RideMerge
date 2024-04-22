#!/usr/bin/env python
import pika
import json


class EmailPublisher:
    def sendToAdmin(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='EmailTopic')

        data = {
            'message': 'Monitoring Message -  ERROR BEING THROWN AT HIGH RATES ',
            'receiver': 'zaidcoder@gmail.com'
        }
        json_data = json.dumps(data)

        channel.basic_publish(exchange='', routing_key='EmailTopic', body=json_data,properties=pika.BasicProperties(delivery_mode=2))
        connection.close()

    # def sendToPassengers(self):
