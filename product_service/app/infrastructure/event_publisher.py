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


def publish_event(exchange: str, event_type: str, data: dict):
    """Publish an event to RabbitMQ using Celery for better reliability and connection management."""
    from celery import Celery

    app = Celery("event_publisher", broker=RABBITMQ_URL)

    @app.task
    def send_event(exchange: str, event_type: str, data: dict):
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

    send_event.delay(exchange, event_type, data)


"""
1. Simple fire-and-forget

2. Logs failure but does not crash the service

3. Uses fanout so multiple subscribers can receive the event

4. Designed for critical events like product creation, updates, deletions

5. In a real system, we might want to implement retries, dead-letter queues, or more robust error handling to ensure reliability.

6. This is a basic implementation. In production, consider using a more robust library like Celery or Kombu for better connection management, retries, and error handling.

7. The event data can be extended to include more context (e.g., user info, timestamps) as needed by other services.

8. Ensure that the RabbitMQ server is properly secured and monitored in a production environment

9. This approach allows for loose coupling between services, enabling them to react to events without direct dependencies.

10. Future events (e.g., product_viewed) can be added in a similar way without changing existing logic, promoting extensibility.

11. This design promotes a clean separation of concerns while enabling powerful integrations across the ecosystem.

12. This is a simple implementation of event publishing. In a production system, you would want to handle potential failures in the event publishing process (e.g., retry logic, dead-letter queues).
"""
