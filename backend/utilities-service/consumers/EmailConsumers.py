import pika
import sys
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver, message):
    sender_email = "pranjali.bishnoi@gmail.com"
    sender_password = "knpjlvpdlyjlwlkd"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 

    # Constructing the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = "RIDE-MERGE NOTIFICATION"

    # Adding the message body
    body = message
    msg.attach(MIMEText(body, 'plain'))

    # Sending the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='EmailTopic')

    def callback(ch, method, properties, body):
        body_str = body.decode('utf-8')
        data = json.loads(body_str)
        print(f" [x] Received {data}")

        print("Sending email to:", data.get('receiver'))
        send_email(data.get('receiver'), data.get('message'))

    channel.basic_consume(queue='EmailTopic', on_message_callback=callback, auto_ack=True)

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
