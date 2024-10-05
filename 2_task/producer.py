import json
import time
from datetime import datetime
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW_Module_8', exchange_type='direct')
channel.queue_declare(queue='hw_queue', durable=True)
channel.queue_bind(exchange='HW_Module_8', queue='hw_queue')


def create_task(nums: int):
    for i in range(nums):
        time.sleep(0.5)
        message = {
            'id': i,
            'payload': f'Date: {datetime.now().isoformat()}',
        }
        channel.basic_publish(exchange='HW_Module_8', routing_key='hw_queue', body=json.dumps(message).encode('utf-8'))
    connection.close()


if __name__ == '__main__':
    create_task(100)
