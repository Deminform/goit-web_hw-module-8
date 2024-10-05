import os
import sys
from datetime import datetime

import pika
from model import Subscriber


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials))
    channel = connection.channel()

    queue = 'phone_number'
    channel.queue_declare(queue=queue, durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        notify = Subscriber.objects(id=pk, sms_sent=False, notify_method=queue).first()
        if notify:
            notify.update(
                set__sms_sent=True,
                push__notify_date={queue: datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

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
