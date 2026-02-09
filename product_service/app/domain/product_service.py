from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.infrastructure.models import Product
from app.core.errors import DomainError
from sqlalchemy.orm import Session


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
        name=product.name, description=product.description, price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ProductResponse(
        id=db.product_id,
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
    )


def list_products(db: Session):
    products = db.query(Product).all()
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

    db.commit()
    db.refresh(product)

    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
    )
