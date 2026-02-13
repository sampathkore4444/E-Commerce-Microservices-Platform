# consumers/event_consumer.py
import pika, json
from app.services.forecasting import update_forecast
from app.services.recommendations import update_user_recommendations

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
        update_forecast(event)
        update_user_recommendations(event)

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    print("ML Analytics service started. Listening for events...")
    channel.start_consuming()
