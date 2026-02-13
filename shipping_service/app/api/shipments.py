# shipping_service/app/api/shipments.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import Shipment
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/shipments", response_model=List[dict])
def list_shipments(db: Session = Depends(get_db)):
    return [s.__dict__ for s in db.query(Shipment).all()]


@router.get("/shipments/{order_id}")
def get_shipment(order_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.order_id == order_id).first()
    if shipment:
        return shipment.__dict__
    return {"message": "Shipment not found"}
