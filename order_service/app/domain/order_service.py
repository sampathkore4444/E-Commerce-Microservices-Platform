from app.core.errors import DomainError
from sqlalchemy.orm import Session
from app.schemas.order import (
    Order,
    OrderItemCreate,
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
)
import requests
from app.infrastructure.event_publisher import publish_event


PRODUCT_SERVICE_URL = "http://localhost:8000/api/v1/products"
PROMOTION_SERVICE_URL = "http://localhost:8001/api/v1/promotions"


class OrderError(DomainError):
    code: str = "ORDER_ERROR"
    message: str = "An error occurred while processing the order"


def create_order(order_data: OrderCreate, db: Session):
    # Validate order data, check product availability, calculate totals, etc.
    # If any validation fails, raise OrderError with a specific message

    total_amount = 0.0
    order_items = []

    for item in order_data.items:
        # Fetch product details from product service
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{item.product_id}")

        if product_response.status_code != 200:
            raise OrderError(message=f"Product {item.product_id} not found")

        product = product_response.json()

        if product["stock"] < item.quantity:
            raise OrderError(
                message=f"Insufficient stock for product {item.product_id}"
            )

        # Fetch active promotions for the product
        r = requests.get(
            f"{PROMOTION_SERVICE_URL}?product_id={item.product_id}&active=true"
        )

        promotions = r.json()
        discount = 0.0
        if promotions:
            # Assume we apply the first active promotion for simplicity
            promo = promotions[0]  # take first active promotion
            if promo["discount_type"] == "fixed":
                discount = promo["discount_value"]  # fixed amount off
            elif promo["discount_type"] == "percentage":
                discount = product["price"] * (promo["discount_value"] / 100)

        unit_price_after_discount = max(product["price"] - discount, 0)

        total_amount += unit_price_after_discount * item.quantity

        order_items.append(
            OrderItemResponse(
                product_id=item.product_id,
                product_name=product["name"],
                unit_price=product["price"],
                quantity=item.quantity,
                discount_applied=discount,
            )
        )

    # Create order record in the database
    db_order = Order(
        user_id=order_data.user_id,
        total_amount=total_amount,
        status="pending",
        items=order_items,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Reduce stock via Product Service
    for item in order_data.items:
        requests.post(
            f"{PRODUCT_SERVICE_URL}/{item.product_id}/stock",
            json={"quantity": -item.quantity},
        )

    # Publish order_created event
    publish_event(
        exchange="orders",
        event_type="order_created",
        data={
            "order_id": db_order.id,
            "user_id": db_order.user_id,
            "total": db_order.total_amount,
        },
    )

    return db_order


"""
✅ Notes:

Stock validation is synchronous here for simplicity

Promotions applied automatically

Event-driven: order_created triggers downstream services (notifications, analytics, etc.)

Stock is decremented via Product Service API → keeps services decoupled
"""
