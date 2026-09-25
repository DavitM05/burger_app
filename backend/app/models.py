from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Burger(Base):
    __tablename__ = "burgers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(6, 2), nullable=False)
    image_url = Column(String(500), nullable=True)
    category = Column(String(60), default="classic")
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order_items = relationship("OrderItem", back_populates="burger")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(120), nullable=False)
    customer_phone = Column(String(40), nullable=True)
    delivery_address = Column(String(255), nullable=True)
    status = Column(String(30), default="pending")  # pending, preparing, out_for_delivery, delivered, cancelled
    total_price = Column(Numeric(8, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    burger_id = Column(Integer, ForeignKey("burgers.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(6, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    burger = relationship("Burger", back_populates="order_items")
