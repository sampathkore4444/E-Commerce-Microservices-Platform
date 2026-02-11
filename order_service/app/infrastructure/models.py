from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from datetime import datetime


class Order(Base):
    __table_name__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(
        String, nullable=False, default="pending"
    )  # pending, paid, cancelled, fulfilled
    payment_status = Column(String, default="unpaid")  # unpaid, paid, failed
    payment_method = Column(String, nullable=True)
    created_at = Column(String, default=datetime.now().isoformat())

    items = relationship(
        "OrderItem", back_populates="order"
    )  # One-to-many relationship with OrderItem


class OrderItem(Base):
    __table_name__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount_applied = Column(Float, default=0.0)

    order = relationship(
        "Order", back_populates="items"
    )  # Many-to-one relationship with Order
