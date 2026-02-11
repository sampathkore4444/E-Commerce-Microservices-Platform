from app.core.errors import DomainError
from sqlalchemy.orm import Session
from app.schemas.promotion import (
    PromotionCreate,
    PromotionResponse,
    PromotionUpdate,
)  # request/response schemas
from app.infrastructure.models import Promotion, Product  # table definition
from app.infrastructure.event_publisher import publish_event  # event publishing


class PromotionNotFound(DomainError):
    code = "PROMOTION_NOT_FOUND"
    message = "Promotion not found"


def create_promotion(promo: PromotionCreate, db: Session) -> PromotionResponse:
    existing = db.query(Promotion).filter(promo.name == promo.name).first()

    if existing:
        raise DomainError(message="Promotion with this name already exists")

    product = db.query(Product).filter(Product.id == promo.product_id).first()

    if not product:
        raise DomainError(message="product not found ")

    db_promo = Promotion(
        name=promo.name,
        description=promo.description,
        discount_percentage=promo.discount_percentage,
        active=promo.active,
        product_id=promo.product_id,
    )
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)

    publish_event(
        exchange="promotions",
        event_type="promotion_created",
        data={"id": db_promo.id, "product_id": db_promo.product_id},
    )

    return PromotionResponse(
        id=db_promo.id,
        name=db_promo.name,
        discount_type=db_promo.discount_type,
        discount_percentage=db_promo.discount_percentage,
        active=db_promo.active,
        product_id=db_promo.product_id,
    )


def list_promotions(db: Session, active_only: bool = True) -> list[PromotionResponse]:
    query = db.query(Promotion)
    if active_only:
        query = query.filter(Promotion.active == True)

    return [
        PromotionResponse(
            id=promo.id,
            name=promo.name,
            discount_type=promo.discount_type,
            discount_percentage=promo.discount_value,
            active=promo.active,
            product_id=promo.product_id,
        )
        for promo in query.all()
    ]


def get_promotions_for_product(
    db: Session, product_id: int, active_only: bool = True
) -> list[PromotionResponse]:
    promos = (
        db.query(Promotion)
        .filter(Promotion.product_id == product_id, Promotion.active == active_only)
        .all()
    )

    return [
        PromotionResponse(
            id=promo.id,
            name=promo.name,
            discount_type=promo.discount_type,
            discount_percentage=promo.discount_value,
            active=promo.active,
            product_id=promo.product_id,
        )
        for promo in promos
    ]


def update_promotion(
    promo_id: int, updates: PromotionUpdate, db: Session
) -> PromotionResponse:
    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()

    if not promo:
        raise PromotionNotFound()

    if updates.name is not None:
        promo.name = updates.name

    if updates.discount_percentage is not None:
        promo.discount_percentage = updates.discount_percentage

    if updates.discount_value is not None:
        promo.discount_value = updates.discount_value

    if updates.active is not None:
        promo.active = updates.active

    db.commit()
    db.refresh(promo)

    publish_event(
        exchange="promotions",
        event_type="promotion_updated",
        data={"id": promo.id, "product_id": promo.product_id},
    )

    return PromotionResponse(
        id=-promo.id,
        name=promo.name,
        discount_type=promo.discount_type,
        discount_percentage=promo.discount_percentage,
        active=promo.active,
        product_id=promo.product_id,
    )


def delete_promotion(promo_id: int, db: Session):
    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()

    if not promo:
        raise PromotionNotFound()

    db.delete(promo)
    db.commit()

    publish_event(
        exchange="promotions",
        event_type="promotion_deleted",
        data={"id": promo.id, "product_id": promo.product_id},
    )
