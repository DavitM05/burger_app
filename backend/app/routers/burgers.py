from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/burgers", tags=["burgers"])


@router.get("/", response_model=List[schemas.Burger])
def list_burgers(available_only: bool = False, db: Session = Depends(get_db)):
    return crud.get_burgers(db, available_only=available_only)


@router.get("/{burger_id}", response_model=schemas.Burger)
def get_burger(burger_id: int, db: Session = Depends(get_db)):
    burger = crud.get_burger(db, burger_id)
    if not burger:
        raise HTTPException(status_code=404, detail="Burger not found")
    return burger


@router.post("/", response_model=schemas.Burger, status_code=201)
def create_burger(burger: schemas.BurgerCreate, db: Session = Depends(get_db)):
    return crud.create_burger(db, burger)


@router.put("/{burger_id}", response_model=schemas.Burger)
def update_burger(burger_id: int, burger: schemas.BurgerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_burger(db, burger_id, burger)
    if not updated:
        raise HTTPException(status_code=404, detail="Burger not found")
    return updated


@router.delete("/{burger_id}", status_code=204)
def delete_burger(burger_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_burger(db, burger_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Burger not found")
    return None
