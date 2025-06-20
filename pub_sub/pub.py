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
        channel.exchange_declare(exchange="logs", exchange_type="fanout")

        message = str(uuid.uuid4())
        channel.basic_publish(exchange="logs", routing_key="", body=message)
        print(f" [x] Sent {message}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
