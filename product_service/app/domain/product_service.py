from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    CategoryResponse,
    TagResponse,
)
from app.infrastructure.models import Product, Tag
from app.core.errors import DomainError
from sqlalchemy.orm import Session
from typing import Optional


class ProductAlreadyExists(DomainError):
    code = "PRODUCT_ALREADY_EXISTS"
    message = "Product with this name already exists"


class ProductNotFound(DomainError):
    code = "PRODUCT_NOT_FOUND"
    message = "Product not found"


def create_product(product: ProductCreate, db: Session) -> ProductResponse:
    existing = db.query(Product).filter(Product.name == product.name).first()
    if existing:
        raise ProductAlreadyExists()

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )

    # Attach tags if provided
    if product.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(product.tag_ids)).all()
        db_product.tags = tags

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return ProductResponse(
        id=db.product_id,
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        category=(
            CategoryResponse(id=db_product.category.id, name=db_product.category.name)
            if product.category_id
            else None
        ),
        tags=[
            TagResponse(id=tag.id, name=tag.name) for tag in db_product.tags
        ],  # Include tags in response
    )


# def list_products(db: Session):
#     products = db.query(Product).all()
#     return [
#         ProductResponse(
#             id=product.id,
#             name=product.name,
#             description=product.description,
#             price=product.price,
#         )
#         for product in products
#     ]

"""Update Domain Logic

✅ Notes:

Uses SQLAlchemy’s ilike for case-insensitive partial matches

Sorting is dynamic but safe (default to id)

Filters are optional — endpoint can list all products if no query params
"""

"""
✅ Notes:

Pagination is fully integrated with filters and sorting

Domain layer still handles all logic — API just passes parameters

Safe defaults and caps prevent abuse
"""


def list_products(
    db: Session,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    sort_by: Optional[str] = "id",
    sort_order: Optional[str] = "asc",
    limit: int = 50,
    offset: int = 0,
):
    products = db.query(Product)

    # Apply filters
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if min_price:
        query = query.filter(Product.price >= min_price)

    if max_price:
        query == query.filter(Product.price <= max_price)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if tag_id:
        query = query.join(Product.tags).filter(Tag.id == tag_id)

    # Apply sorting
    sort_column = getattr(Product, sort_by, Product.id)
    if sort_order.lower() == "desc":
        sort_column = sort_column.desc()

    query = query.order_by(sort_column)

    # Apply pagination
    query = query.offset(offset).limit(limit)

    products = query.all()

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
        )
        for product in products
    ]


def delete_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise DomainError(message="Product not found")
    db.delete(product)
    db.commit()


def update_product(product_id: int, updates: ProductUpdate, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ProductNotFound()

    # Check uniqueness if name is changing
    if updates.name and updates.name != product.name:
        existing = db.query(Product).filter(Product.name == updates.name).first()
        if existing:
            raise ProductAlreadyExists()

    # Apply updates
    if updates.name is not None:
        product.name = updates.name

    if updates.description is not None:
        product.description = updates.description

    if updates.price is not None:
        product.price = updates.price

    if updates.category_id is not None:
        product.category_id = updates.category_id

    if updates.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(updates.tag_ids)).all()
        product.tags = tags

    db.commit()
    db.refresh(product)

    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=(
            CategoryResponse(id=product.category.id, name=product.category.name)
            if product.category_id
            else None
        ),
        tags=[
            TagResponse(id=tag.id, name=tag.name) for tag in product.tags
        ],  # Include tags in response
    )
