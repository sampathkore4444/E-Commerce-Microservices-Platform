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
