from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

Base = DeclarativeBase()


class OrderAnalytics(Base):
    __tablename__ = "order_analytics"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    payment_status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())


class ProductAnalytics(Base):
    __tablename__ = "product_analytics"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    tags = Column(String, nullable=True)  # Comma-separated tags
    active_promotions = Column(String, nullable=True)  # Comma-separated promotion IDs
