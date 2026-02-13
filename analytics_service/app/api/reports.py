from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.models import OrderAnalytics, ProductAnalytics
from typing import List, Dict

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products")
def get_product_analytics(db: Session = Depends(get_db)) -> List[Dict]:
    products = db.query(ProductAnalytics).all()
    # return [p.to_dict() for p in products]
    return [
        {
            "product_id": p.product_id,
            "name": p.name,
            "stock": p.stock,
            "price": p.price,
            "category": p.category,
        }
        for p in products
    ]


@router.get("/orders")
def get_order_analytics(db: Session = Depends(get_db)) -> List[Dict]:
    orders = db.query(OrderAnalytics).all()
    # return [p.to_dict() for p in orders]
    return [
        {
            "order_id": o.order_id,
            "user_id": o.user_id,
            "total_amount": o.total_amount,
            "status": o.status,
            "payment_status": o.payment_status,
        }
        for o in orders
    ]


@router.get("/revenue")
def get_revenue_analytics(db: Session = Depends(get_db)) -> Dict:
    total_revenue = (
        db.query(OrderAnalytics)
        .filter(OrderAnalytics.payment_status == "paid")
        .with_entities(func.sum(OrderAnalytics.total_amount))
        .scalar()
        or 0.0
    )
    return {"total_revenue": total_revenue}
