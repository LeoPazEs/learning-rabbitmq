import os
import sys
import time

import pika


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    time.sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost", credentials=pika.credentials.PlainCredentials("admin", "admin")
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="hello", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="hello", on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
