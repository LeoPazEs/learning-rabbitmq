import os
import sys
import uuid

import pika


def main():
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost", credentials=pika.credentials.PlainCredentials("admin", "admin")
        )
    ) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

        routing_key = sys.argv[1] if len(sys.argv) > 1 else "anonymous.info"
        message = str(uuid.uuid4())
        channel.basic_publish(
            exchange="topic_logs", routing_key=routing_key, body=message
        )
        print(f" [x] Sent {routing_key}:{message}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
