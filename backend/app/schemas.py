from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# ---------- Burger ----------

class BurgerBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    category: Optional[str] = "classic"
    is_available: Optional[bool] = True


class BurgerCreate(BurgerBase):
    pass


class BurgerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None


class Burger(BurgerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------- Order ----------

class OrderItemCreate(BaseModel):
    burger_id: int
    quantity: int = 1


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    burger_id: int
    quantity: int
    unit_price: Decimal
    burger: Optional[Burger] = None


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_name: str
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    status: str
    total_price: Decimal
    created_at: datetime
    items: List[OrderItemOut] = []
