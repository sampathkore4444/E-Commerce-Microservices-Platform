# shipping_service/app/consumers/event_consumer.py

import pika, json
from app.services.shipping_service import create_shipment, cancel_shipment
from app.core.config import RABBITMQ_URL

EXCHANGES = ["orders"]


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    for exchange in EXCHANGES:
        channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        queue = channel.queue_declare(queue="", exclusive=True).method.queue
        channel.queue_bind(exchange=exchange, queue=queue)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        event_type = event.get("event_type")
        data = event.get("data")

        if event_type == "order_paid":
            create_shipment(data)
        elif event_type == "order_cancelled":
            cancel_shipment(data["order_id"])

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    print("Shipping service started. Listening for events...")
    channel.start_consuming()
