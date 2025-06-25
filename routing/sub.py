import os
import sys

import pika
from logs_levels import levels


def main():
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost", credentials=pika.credentials.PlainCredentials("admin", "admin")
        )
    ) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

        queue = channel.queue_declare(queue="", exclusive=True)
        queue_name = queue.method.queue

        severity = [int(v) for v in sys.argv[1:]]
        if not severity:
            sys.stderr.write("Usage: %s 0-> info 1-> warning 2-> error\n" % sys.argv[0])
            sys.exit(1)

        for sev in severity:
            channel.queue_bind(
                exchange="direct_logs", queue=queue_name, routing_key=levels[sev]
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
