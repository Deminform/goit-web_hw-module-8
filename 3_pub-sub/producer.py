import json
import time
from datetime import datetime
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Events message', exchange_type='fanout')
# channel.queue_declare(queue='hw_queue', durable=True)
# channel.queue_bind(exchange='Events message', queue='hw_queue')


def create_event():
    message = {
        'event': 'Test event',
        'message': 'Some test message',
        'payload': f'Date: {datetime.now().isoformat()}',
    }
    channel.basic_publish(exchange='Events message', routing_key='', body=json.dumps(message).encode())
    connection.close()


if __name__ == '__main__':
    create_event()
