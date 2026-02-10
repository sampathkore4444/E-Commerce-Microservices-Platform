from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.domain.product_service import (
    create_product,
    list_products,
    delete_product,
    update_product,
    adjust_stock,
)
from app.infrastructure.database import SessionLocal
from app.api.dependencies import admin_required
from typing import Optional
from pydantic import BaseModel


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
def create_product_endpoint(
    product: ProductCreate, db: Session = Depends(get_db), user=Depends(admin_required)
):
    return create_product(product, db)


# @router.get("/", response_model=list[ProductResponse])
# def list_products_endpoint(db: Session = Depends(get_db)):
#     return list_products(db)


@router.get("/", response_model=list[ProductResponse])
def list_products_endpoint(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by product name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    category_id: Optional[int] = Query(None),
    tag_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("id", description="Sort field:id, name, price"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    limit: int = Query(50, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip"),
):
    """Search & Filtering Products

    We want:

    Endpoint: GET /api/v1/products (reuse the listing endpoint)

    Filters:

    name (partial match)

    min_price / max_price

    Sorting: Optional, e.g., by price or name

    Pagination: Optional, to prepare for large datasets"""

    return list_products(
        db,
        name,
        min_price,
        max_price,
        sort_by,
        sort_order,
        limit,
        offset,
        category_id,
        tag_id,
    )


@router.delete("/{product_id}", status_code=204)
def delete_product_endpoint(
    product_id: int, db: Session = Depends(get_db), user=Depends(admin_required)
):
    return delete_product(product_id, db)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(admin_required),
):
    return update_product(product_id, updates, db)


class StockAdjustment(BaseModel):
    quantity: int  # positive or negative


@router.post("/{product_id}/stock", status_code=200)
def adjust_stock_endpoint(
    product_id: int,
    adjustment: StockAdjustment,
    db: Session = Depends(get_db),
    user=Depends(admin_required),
):
    """Endpoint to update stock levels

    This allows admins to adjust inventory levels directly.

    The quantity can be positive (to add stock) or negative (to remove stock).

    Endpoint allows increment or decrement

    Only admins can modify stock
    """

    return adjust_stock(product_id, adjustment.quantity, db)


"""Only admins can create/update/delete

Public users can still GET /products"""
