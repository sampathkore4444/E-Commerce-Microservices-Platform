from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.domain.product_service import (
    create_product,
    list_products,
    delete_product,
    update_product,
)
from app.infrastructure.database import SessionLocal
from typing import Optional

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


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)


# @router.get("/", response_model=list[ProductResponse])
# def list_products_endpoint(db: Session = Depends(get_db)):
#     return list_products(db)


"""Search & Filtering Products

We want:

Endpoint: GET /api/v1/products (reuse the listing endpoint)

Filters:

name (partial match)

min_price / max_price

Sorting: Optional, e.g., by price or name

Pagination: Optional, to prepare for large datasets"""


@router.get("/", response_model=list[ProductResponse])
def list_products_endpoint(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by product name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    sort_by: Optional[str] = Query("id", description="Sort field:id, name, price"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
):
    return list_products(db, name, min_price, max_price, sort_by, sort_order)


@router.delete("/{product_id}", status_code=204)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id, db)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)
):
    return update_product(product_id, updates, db)
