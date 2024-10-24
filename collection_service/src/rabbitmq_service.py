import pika, json

params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='hello')

#exchange definieren; Exchange für collection_service_exchange benennen
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

print(" [x] Sent 'Hello World!'")
#connection.close()

def publishEvent(method, body = 'Hello World'):
    #properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='hello', \
    body=json.dumps(body))  
    #, properties=properties) 