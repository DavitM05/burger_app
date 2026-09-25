from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Burgers ----------

def get_burgers(db: Session, available_only: bool = False):
    q = db.query(models.Burger)
    if available_only:
        q = q.filter(models.Burger.is_available == True)  # noqa: E712
    return q.order_by(models.Burger.id).all()


def get_burger(db: Session, burger_id: int):
    return db.query(models.Burger).filter(models.Burger.id == burger_id).first()


def create_burger(db: Session, burger: schemas.BurgerCreate):
    db_burger = models.Burger(**burger.model_dump())
    db.add(db_burger)
    db.commit()
    db.refresh(db_burger)
    return db_burger


def update_burger(db: Session, burger_id: int, burger: schemas.BurgerUpdate):
    db_burger = get_burger(db, burger_id)
    if not db_burger:
        return None
    for field, value in burger.model_dump(exclude_unset=True).items():
        setattr(db_burger, field, value)
    db.commit()
    db.refresh(db_burger)
    return db_burger


def delete_burger(db: Session, burger_id: int):
    db_burger = get_burger(db, burger_id)
    if not db_burger:
        return None
    db.delete(db_burger)
    db.commit()
    return db_burger


# ---------- Orders ----------

def create_order(db: Session, order: schemas.OrderCreate):
    total = 0
    db_order = models.Order(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        status="pending",
        total_price=0,
    )
    db.add(db_order)
    db.flush()  # get db_order.id before commit

    for item in order.items:
        burger = get_burger(db, item.burger_id)
        if not burger:
            continue
        unit_price = burger.price
        total += float(unit_price) * item.quantity
        db_item = models.OrderItem(
            order_id=db_order.id,
            burger_id=item.burger_id,
            quantity=item.quantity,
            unit_price=unit_price,
        )
        db.add(db_item)

    db_order.total_price = total
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order_status(db: Session, order_id: int, status: str):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order
