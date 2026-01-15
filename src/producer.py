import pika
import os

def send_message(message: str, host: str = None, queue: str = 'hello'):
    if host is None:
        host = os.getenv('RABBITMQ_HOST', 'localhost')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message)
    print(f" [x] Sent '{message}'")
    connection.close()

if __name__ == "__main__":
    send_message("Hello World!")
