#!/usr/bin/env python
import pika


class SMSPublisher:
    def sendToAdmin(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='SMSTopic')

        channel.basic_publish(exchange='', routing_key='SMSTopic', body='wello',properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
