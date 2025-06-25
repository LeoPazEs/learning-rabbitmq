import os
import sys
import uuid

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

        severity = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        message = str(uuid.uuid4())
        channel.basic_publish(
            exchange="direct_logs", routing_key=levels[severity], body=message
        )
        print(f" [x] Sent {levels[severity]}:{message}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
