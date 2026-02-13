# audit_service/app/consumers/event_consumer.py

import pika, json
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import EventLog

EXCHANGES = ["orders", "products", "promotions", "shipments", "payments"]


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    for exchange in EXCHANGES:
        channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        queue = channel.queue_declare(queue="", exclusive=True).method.queue
        channel.queue_bind(exchange=exchange, queue=queue)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        db: Session = SessionLocal()
        try:
            log = EventLog(
                service=exchange,
                event_type=event.get("event_type"),
                payload=json.dumps(event.get("data")),
            )
            db.add(log)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[AUDIT] Failed to log event: {e}")
        finally:
            db.close()

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    print("Audit service started. Listening for events...")
    channel.start_consuming()
