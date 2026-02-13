import pika, json
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.services.analytics_service import process_event
from app.core.config import RABBITMQ_URL

EXCHANGES = ["orders", "products", "promotions"]


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
            process_event(event, db)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ANALYTICS] Failed to process event: {e}")
        finally:
            db.close()

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    print("Analytics service started. Listening for events...")
    channel.start_consuming()
