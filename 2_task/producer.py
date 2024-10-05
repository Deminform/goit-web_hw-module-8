import random
import pika
from faker import Faker
from model import Subscriber


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=credentials))
channel = connection.channel()

fake = Faker()
exchange = 'Change of conditions'
queue_sms = 'phone_number'
queue_email = 'email'


channel.exchange_declare(exchange=exchange, exchange_type='direct')
channel.queue_declare(queue=queue_sms, durable=True)
channel.queue_declare(queue=queue_email, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_sms)
channel.queue_bind(exchange=exchange, queue=queue_email)


def notify_all(nums: int):
    for i in range(nums):
        notification = Subscriber(
            fullname=fake.name(),
            email=fake.email(),
            phone_number=str(fake.basic_phone_number()),
            notify_method=random.sample(['email', 'phone_number'], k=random.randint(1, 2)),
        ).save()

        for queue in notification.notify_method:
            channel.basic_publish(
                exchange=exchange,
                routing_key=queue,
                body=str(notification.id).encode(),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
        print(f' [v] Notification {i} sent')
    connection.close()


if __name__ == '__main__':
    notify_all(30)
