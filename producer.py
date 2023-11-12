import json
from datetime import datetime

import pika
from mongoengine import connect
from contact_model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Web16 exchange', exchange_type='direct')
channel.queue_declare(queue='web_16_queue', durable=True)
channel.queue_bind(exchange='Web16 exchange', queue='web_16_queue')

def create_tasks(nums: int):
    for _ in range(nums):
        # Збереження контакту в базі даних
        contact = Contact.create_fake_contact()
        contact.save()

        message = {
            'contact_id': str(contact.id),
            'payload': f"Date: {datetime.now().isoformat()}"
        }

        channel.basic_publish(exchange='Web16 exchange', routing_key='web_16_queue', body=json.dumps(message).encode())

    connection.close()

if __name__ == '__main__':
    create_tasks(50)
