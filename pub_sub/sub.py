import os
import sys

import pika


def main():
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost", credentials=pika.credentials.PlainCredentials("admin", "admin")
        )
    ) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange="logs", exchange_type="fanout")

        queue = channel.queue_declare(queue="", exclusive=True)
        queue_name = queue.method.queue

        channel.queue_bind(exchange="logs", queue=queue_name)
        print(" [*] Waiting for logs. To exit press CTRL+C")

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        channel.start_consuming()


def callback(ch, method, properties, body):
    print(f" [x] {body}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
