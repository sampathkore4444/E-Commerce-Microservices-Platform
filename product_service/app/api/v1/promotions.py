from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.promotion import PromotionCreate, PromotionUpdate, PromotionResponse
from app.domain.promotion_service import (
    create_promotion,
    list_promotions,
    update_promotion,
    delete_promotion,
)
from app.infrastructure.database import SessionLocal
from app.api.dependencies import admin_required

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


@router.post("/", response_model=PromotionResponse)
def create_promotion_endpoint(
    promo: PromotionCreate,
    db: Session = Depends(get_db),
    user=Depends(admin_required),
):
    return create_promotion(promo, db)


@router.get("/", response_model=List[PromotionResponse])
def list_promotions_endpoint(db: Session = Depends(get_db)):
    return list_promotions(db)


@router.patch("/{promo_id}", response_model=PromotionResponse)
def update_promotion_endpoint(
    promo_id: int,
    updates: PromotionUpdate,
    db: Session = Depends(get_db),
    user=Depends(admin_required),
):
    return update_promotion(promo_id, updates, db)


@router.delete("/{promo_id}", status_code=204)
def delete_promotion_endpoint(
    promo_id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required),
):
    delete_promotion(promo_id, db)
