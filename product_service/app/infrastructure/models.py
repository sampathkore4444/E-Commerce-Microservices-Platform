from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.database import Base


class Product(Base):
    __table__name = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
