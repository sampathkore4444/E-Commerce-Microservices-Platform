from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

# Many-to-many association table for products and tags
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Category(Base):
    __table_name__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Tag(Base):
    __table_name__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Product(Base):
    __table__name = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)  # New field

    category_id = Column(Integer, ForeignKey("categories.id", nullable=True))
    category = relationship("Category")

    tags = relationship("Tag", secondary="product_tags", back_populates="products")


"""✅ Notes:

One-to-many: Product → Category

Many-to-many: Product ↔ Tags

Backrefs allow easy reverse lookup

"""

"""
1. stock defaults to 0

2. Updated ORM for atomic updates

3. In a real system, we might want to implement more complex inventory management (e.g., reserved stock, backorders)
"""


class User(Base):
    __table__name = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)
    role = Column(String, default="user")  # "user" or "admin"
    is_active = Column(Boolean, default=True)


"""
now we’ll implement Promotions & Discounts, which is essential for an e-commerce product service. We’ll design it in a clean, extensible way so future promo types can be added without breaking the API.

Step 9 — Promotions & Discounts

Goals:

Support multiple discount types:

Fixed amount (e.g., $20 off)

Percentage (e.g., 10% off)

Apply discounts per product

Ensure stackable rules are handled correctly

Expose endpoints to create, update, list, and remove promotions

Optionally publish events when promotions change
"""


class Promotion(Base):
    """
    Each promotion belongs to one product

    discount_type distinguishes between fixed and percentage discounts

    active allows enabling/disabling promotions
    """

    __table_name__ = "promotions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    discount_type = Column(String, nullable=False)  # "Fixed" or "Percentage"
    discount_value = Column(
        Float, nullable=False
    )  # e.g., 20 for $20 off or 10 for 10% off
    active = Column(Boolean, default=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Relationship back to Parent (Product)
    product = relationship("Product", back_populates="promotions")
