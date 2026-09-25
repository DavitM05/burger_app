from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])

VALID_STATUSES = {"pending", "preparing", "out_for_delivery", "delivered", "cancelled"}


@router.post("/", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")
    return crud.create_order(db, order)


@router.get("/", response_model=List[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, payload: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Status must be one of {sorted(VALID_STATUSES)}")
    order = crud.update_order_status(db, order_id, payload.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
