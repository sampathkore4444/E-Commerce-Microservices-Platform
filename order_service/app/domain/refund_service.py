# order_service/app/domain/refund_service.py

from sqlalchemy.orm import Session
from app.infrastructure.models import Order
from app.infrastructure.event_publisher import publish_event


def request_refund(order_id: int, reason: str, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")
    if order.status not in ["paid", "fulfilled"]:
        raise ValueError("Order cannot be refunded")

    order.refund_status = "requested"
    order.status = "cancelled"
    db.commit()
    db.refresh(order)

    # Return stock to Product Service
    for item in order.items:
        # call Product Service API to increment stock
        pass  # existing logic

    # Publish refund event
    publish_event("orders", "order_refunded", {"order_id": order.id, "reason": reason})

    return order
