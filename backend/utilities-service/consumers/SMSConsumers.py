# #!/usr/bin/env python
# import pika, sys, os
# import json

# def main():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()

#     channel.queue_declare(queue='SMSTopic')

#     def callback(ch, method, properties, body):
#         body_str = body.decode('utf-8')
#         data = json.loads(body_str)
#         print(f" [x] Received {data}")

#         print("this will be sent to appropriate phone number")
#         channel.basic_consume(queue='SMSTopic', on_message_callback=callback, auto_ack=True)

#     channel.basic_consume(queue='SMSTopic', on_message_callback=callback, auto_ack=True)

#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
#!/usr/bin/env python
import pika
import sys
import os
import json
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC60c73da897bc9ecf11c5b520c7efc6fc'
TWILIO_AUTH_TOKEN = 'd22599d999ebfb359505b438bc37a029'
TWILIO_PHONE_NUMBER = '+12513125767'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(receiver, message):
    try:
        message = client.messages.create(
            to='+917992381519',
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print("SMS sent successfully to:", receiver)
    except Exception as e:
        print("Error occurred while sending SMS:", str(e))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='SMSTopic')

    def callback(ch, method, properties, body):
        body_str = body.decode('utf-8')
        data = json.loads(body_str)
        print(f" [x] Received {data}")

        send_sms(data.get('receiver'), data.get('message'))
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
