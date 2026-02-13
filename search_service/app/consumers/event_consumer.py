"""
- Updates the index in real-time
- Reacts to both product and promotion events

    - product_created
    - product_updated
    - product_stock_updated
    - product_deleted
    - promotion_created
    - promotion_updated
    - promotion_deleted

- Uses RabbitMQ for event-driven communication
- Ensures the search index is always up-to-date with the latest product and promotion information

# This code defines a consumer for a search and indexing service in an e-commerce microservices platform.
# The consumer listens to events related to products and promotions, and updates the search index accordingly.

"""

import pika, json
from app.services.indexing_service import add_or_update_product, remove_product, INDEX
from app.core.config import RABBITMQ_URL

EXCHANGES = ["products", "promotions"]


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    for exchange in EXCHANGES:
        channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        queue = channel.queue_declare(queue="", exclusive=True).method.queue
        channel.queue_bind(exchange=exchange, queue=queue)

    def callback(
        ch, method, properties, body
    ):  # why ch, method, properties? - these are parameters required by the pika library for the callback function. They provide information about the channel, the method that triggered the callback, message properties, and the message body itself.
        event = json.loads(body)  # Parse the incoming event data as JSON.
        event_type = event.get("event_type")
        data = event.get("data")

        if event_type in [
            "product_created",
            "product_updated",
            "product_stock_updated",
        ]:
            add_or_update_product(data)
        elif event_type == "product_deleted":
            remove_product(data["id"])
        elif event_type in [
            "promotion_created",
            "promotion_updated",
            "promotion_deleted",
        ]:
            product_id = data.get("product_id")
            if product_id and product_id in INDEX:
                add_or_update_product(INDEX[product_id])  # update promotions
        else:
            print(f"[INDEX] Unknown event: {event_type}")

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    print("Search & Indexing service started. Listening for events...")
    channel.start_consuming()
