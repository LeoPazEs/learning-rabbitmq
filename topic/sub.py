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
        channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

        queue = channel.queue_declare(queue="", exclusive=True)
        queue_name = queue.method.queue

        routing_key = sys.argv[1:]
        if not routing_key:
            sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
            sys.exit(1)

        for rout in routing_key:
            channel.queue_bind(
                exchange="topic_logs", queue=queue_name, routing_key=rout
            )
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
