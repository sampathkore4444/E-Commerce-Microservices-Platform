from app.infrastructure.models import Order
from sqlalchemy.orm import Session
from app.infrastructure.event_publisher import publish_event


def process_payment(order: Order, method: str, token: str) -> bool:
    """
    Simulate payment processing.
    Replace with real gateway SDK (Stripe, PayPal, etc.)
    """
    # Example simulation
    if token.startswith("Fail"):
        return False

    return True


def checkout_order(order_id: int, payment_method: str, payment_token: str, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")

    if order.payment_status == "paid":
        raise ValueError("Order already paid")

    success = process_payment(order, payment_method, payment_token)

    if success:
        order.payment_status = "paid"
        order.status = "fulfilled"
        order.payment_method = payment_method
    else:
        order.payment_status = "failed"
        order.status = "pending"

    db.commit()
    db.refresh(order)

    # publish order_paid or order_payment_failed_events
    event_type = "order_paid" if success else "order_payment_failed"

    publish_event(
        exchange="orders",
        event_type=event_type,
        data={
            "order_id": order.id,
            "user_id": order.user_id,
            "total": order.total_amount,
            "status": order.status,
        },
    )

    return order


"""
✅ Notes:

Payment processing is decoupled; can swap gateways

Events inform inventory, notifications, analytics services
"""
