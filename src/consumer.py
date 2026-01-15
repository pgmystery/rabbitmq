import pika
import os

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

def start_consumer(host: str = None, queue: str = 'hello'):
    if host is None:
        host = os.getenv('RABBITMQ_HOST', 'localhost')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue,
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            import sys
            sys.exit(0)
        except SystemExit:
            os._exit(0)
