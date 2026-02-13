# shipping_service/app/services/shipping_service.py

from sqlalchemy.orm import Session
from app.infrastructure.models import Shipment
from app.infrastructure.database import SessionLocal
from app.infrastructure.event_publisher import publish_event
import random


def create_shipment(order_data: dict):
    db: Session = SessionLocal()
    try:
        shipment = Shipment(
            order_id=order_data["order_id"],
            status="shipped",
            carrier=random.choice(["UPS", "FedEx", "DHL"]),
            tracking_number=f"TRK{random.randint(100000, 999999)}",
        )
        db.add(shipment)
        db.commit()
        db.refresh(shipment)

        # Publish shipment event
        publish_event(
            "shipments",
            "shipment_created",
            {
                "shipment_id": shipment.id,
                "order_id": shipment.order_id,
                "status": shipment.status,
                "carrier": shipment.carrier,
                "tracking_number": shipment.tracking_number,
            },
        )
    finally:
        db.close()


def cancel_shipment(order_id: int):
    db: Session = SessionLocal()
    try:
        shipment = db.query(Shipment).filter(Shipment.order_id == order_id).first()
        if shipment:
            shipment.status = "cancelled"
            db.commit()
            publish_event("shipments", "shipment_cancelled", {"order_id": order_id})
    finally:
        db.close()
