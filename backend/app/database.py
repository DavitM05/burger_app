import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DB_USER = os.getenv("MYSQL_USER", "burger_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "burger_pass")
DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "burger_db")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def wait_for_db(retries: int = 20, delay: float = 3.0):
    """Retry connecting until MySQL is ready (useful on first docker-compose up)."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(__import__("sqlalchemy").text("SELECT 1"))
            return
        except OperationalError:
            print(f"Database not ready yet (attempt {attempt}/{retries}), retrying...")
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database after several retries.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
