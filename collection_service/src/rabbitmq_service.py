import pika, json
import os

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
rabbitmq_host = os.getenv('RABBITMQ_HOST')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
params = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

connection = pika.BlockingConnection(params)
#params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
#connection = pika.BlockingConnection(params)


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
        channel.basic_publish(exchange=exchange, routing_key=method, body=json.dumps(body))
        
        

# def callback(ch, method, properties, body):
#         print(f" [x] Received {body}", flush=True)
#         create_notification(ch, method, properties, body)
      
#channel.basic_consume(queue='collection.updated', on_message_callback=callback, auto_ack=True)
#channel.start_consuming()
    
                    