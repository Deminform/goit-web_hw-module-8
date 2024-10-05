import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hw_queue')

message = 'Hello Again!'
channel.basic_publish(exchange='', routing_key='hw_queue', body=message)
print(f' [x] Sent "{message}"')
connection.close()
