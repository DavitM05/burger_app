from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, wait_for_db, SessionLocal
from .routers import burgers, orders

app = FastAPI(title="Burger House API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(burgers.router)
app.include_router(orders.router)


SEED_BURGERS = [
    dict(
        name="Classic Cheeseburger",
        description="Beef patty, cheddar, lettuce, tomato, house sauce, brioche bun.",
        price=8.50,
        image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
        category="classic",
    ),
    dict(
        name="Smoky BBQ Bacon Burger",
        description="Beef patty, crispy bacon, smoked cheddar, onion rings, BBQ sauce.",
        price=10.90,
        image_url="https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600",
        category="signature",
    ),
    dict(
        name="Spicy Jalapeño Burger",
        description="Beef patty, pepper jack, jalapeños, chipotle mayo, pickled onions.",
        price=9.75,
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349?w=600",
        category="spicy",
    ),
    dict(
        name="Mushroom Swiss Burger",
        description="Beef patty, sautéed mushrooms, swiss cheese, garlic aioli.",
        price=9.90,
        image_url="https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600",
        category="signature",
    ),
    dict(
        name="Garden Veggie Burger",
        description="Grilled plant-based patty, avocado, sprouts, vegan aioli, whole wheat bun.",
        price=8.90,
        image_url="https://images.unsplash.com/photo-1520072959219-c595dc870360?w=600",
        category="vegetarian",
    ),
    dict(
        name="Double Stack Deluxe",
        description="Two beef patties, double cheddar, caramelized onions, burger sauce.",
        price=12.50,
        image_url="https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600",
        category="signature",
    ),
]


@app.on_event("startup")
def on_startup():
    wait_for_db()
    models.Base.metadata.create_all(bind=engine)

    # Seed the menu once if the table is empty
    db = SessionLocal()
    try:
        if db.query(models.Burger).count() == 0:
            for item in SEED_BURGERS:
                db.add(models.Burger(**item))
            db.commit()
    finally:
        db.close()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Burger House API — see /docs for the interactive API reference."}
