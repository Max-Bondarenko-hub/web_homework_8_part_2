import connect
import json
import pika
from models import Clients

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="sender_queue", durable=True)


def stub_mailing(client_id):
    client = Clients.objects(id=client_id)
    # Sending email code...
    client.update(sended=True)
    return f"e-mail sended"

print("--- Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f"-- Received {message}")
    result = stub_mailing(message["id"])
    print(result)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="sender_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
