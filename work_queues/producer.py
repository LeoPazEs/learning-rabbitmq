import sys

import pika

message = " ".join(sys.argv[1:]) or "Hello World!"
with pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost", credentials=pika.credentials.PlainCredentials("admin", "admin")
    ),
) as connection:
    channel = connection.channel()
    channel.queue_declare(queue="hello", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )
    print(f" [x] Sent {message}")
