import json
import pika
import logging

logger = logging.getLogger(__name__)

RABBITMQ_URL = "amqp://admin:admin123@localhost:5672/"


def publish_event(exchange: str, event_type: str, data: dict):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type="fanout")

        event = {"event_type": event_type, "data": data}

        channel.basic_publish(
            exchange=exchange,
            routing_key="",
            body=json.dumps(event),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # make message persistent
            ),
        )
        logger.info(f"Published event: {event_type} to exchange: {exchange}")
        connection.close()

    except Exception as e:
        logger.error(f"Failed to publish event {event_type}: {e}")
