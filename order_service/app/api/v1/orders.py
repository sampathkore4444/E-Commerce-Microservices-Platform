from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse
from app.domain.order_service import create_order
from app.infrastructure.database import SessionLocal
from app.api.dependencies import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


@router.post("/", response_model=OrderResponse)
def create_order_endpoint(
    order: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return create_order(order, db)


"""
Any authenticated user can create an order

Domain logic handles stock checks and promotions
"""
