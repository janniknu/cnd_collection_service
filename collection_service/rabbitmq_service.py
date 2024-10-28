import pika, json

params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
connection = pika.BlockingConnection(params)
exchange = 'collection_service_exchange'
channel = connection.channel()

#Nur zum Debuggen
channel.queue_declare(queue='collection.created')
channel.queue_declare(queue='collection.updated')
channel.queue_declare(queue='collection.deleted')

channel.exchange_declare(exchange=exchange, exchange_type='direct')

#Nur zum Debuggen
channel.queue_bind(exchange=exchange,queue='collection.created',routing_key='collection.created')
channel.queue_bind(exchange=exchange,queue='collection.updated',routing_key='collection.updated')
channel.queue_bind(exchange=exchange,queue='collection.deleted',routing_key='collection.deleted')

def publishEvent(method, body):
    #properties = pika.BasicProperties(method)
        channel.basic_publish(exchange=exchange, routing_key=method, body=json.dumps(body))

    #channel.basic_publish(exchange=exchange, routing_key='hello', body=json.dumps(body + method), properties=properties) 