import json
import os
import sys
import time

import pika
from contact_model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='web_16_queue', durable=True)

def send_email(contact_id):
    # Логіка для імітації відправлення email
    print(f"Simulating sending email to contact_id: {contact_id}")

def main():
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        contact_id = message.get('contact_id')
        print(f" [x] Received message for contact_id: {contact_id}")

        # Завантаження контакту з бази даних
        contact = Contact.objects.get(id=contact_id)
        if not contact.is_message_sent:
            # Відправлення email та оновлення статусу в базі даних
            send_email(contact_id)
            contact.is_message_sent = True
            contact.save()

        time.sleep(0.5)
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='web_16_queue', on_message_callback=callback)

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
