import connect
import pika
from gen_and_seed import fill_mongodb_fake_data
from json_enc import JSONEncoder
from models import Clients


NUMBER_OF_CLIENTS = 10

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="my_ex", exchange_type="direct")
channel.queue_declare(queue="sender_queue", durable=True)
channel.queue_bind(exchange="my_ex", queue="sender_queue")


def main():
    Clients.drop_collection()

    for _ in range(NUMBER_OF_CLIENTS):
        client = Clients()
        fill_mongodb_fake_data(client)

    clients = Clients.objects()

    for client in clients:
        message = {"id": client.id}

        channel.basic_publish(
            exchange="my_ex",
            routing_key="sender_queue",
            body=JSONEncoder().encode(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
        print(f"--- Sent: {message}")
    connection.close()


if __name__ == "__main__":
    main()
