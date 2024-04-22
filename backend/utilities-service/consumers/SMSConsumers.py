#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='SMSTopic')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        print("this will be sent to appropriate phone number")
        channel.basic_consume(queue='SMSTopic', on_message_callback=callback, auto_ack=True)

    channel.basic_consume(queue='SMSTopic', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)