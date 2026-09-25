# 🍔 Burger House

A full-stack burger ordering site: browse a menu, build a cart, and place an
order.

- **Frontend:** React (Create React App), served in production by nginx
- **Backend:** FastAPI (Python), SQLAlchemy ORM
- **Database:** MySQL 8
- **Containerization:** Docker
- **Orchestration:** Docker Compose

## Project structure

```
burger-app/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py          # FastAPI app, CORS, startup seeding
│       ├── database.py      # SQLAlchemy engine/session
│       ├── models.py        # ORM models (Burger, Order, OrderItem)
│       ├── schemas.py       # Pydantic request/response schemas
│       ├── crud.py          # DB access functions
│       └── routers/
│           ├── burgers.py   # /api/burgers endpoints
│           └── orders.py    # /api/orders endpoints
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── public/index.html
    └── src/
        ├── App.js, App.css, index.js, index.css
        ├── api.js            # fetch wrapper for the backend API
        └── components/
            ├── Header.js
            ├── Hero.js
            ├── BurgerGrid.js
            ├── CartDrawer.js
            ├── CheckoutForm.js
            └── OrderConfirmation.js
```

## Running it

You need Docker and Docker Compose installed. From the `burger-app/`
directory:

```bash
cp .env.example .env   # optional — defaults work out of the box
docker compose up --build
```

Then open:

- **Frontend:** http://localhost:3000
- **Backend API docs (Swagger):** http://localhost:8000/docs
- **MySQL:** localhost:3306 (user/db from `.env`)

On first boot the backend waits for MySQL to become healthy, creates the
tables, and seeds six starter burgers into the menu automatically — nothing
manual required.

To stop everything: `docker compose down` (add `-v` to also wipe the MySQL
data volume).

## API overview

| Method | Path                        | Description                     |
|--------|-----------------------------|----------------------------------|
| GET    | `/api/burgers/`             | List burgers (`?available_only=true`) |
| GET    | `/api/burgers/{id}`         | Get one burger                  |
| POST   | `/api/burgers/`             | Create a burger                 |
| PUT    | `/api/burgers/{id}`         | Update a burger                 |
| DELETE | `/api/burgers/{id}`         | Delete a burger                 |
| POST   | `/api/orders/`              | Place an order (name + items)   |
| GET    | `/api/orders/`               | List all orders                 |
| GET    | `/api/orders/{id}`          | Get one order                   |
| PATCH  | `/api/orders/{id}/status`   | Update order status             |

Full interactive docs are at `/docs` once the backend is running.

## Local development without Docker

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# point at a local/reachable MySQL, e.g.:
export MYSQL_HOST=localhost MYSQL_USER=burger_user MYSQL_PASSWORD=burger_pass MYSQL_DATABASE=burger_db
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm start   # proxies /api to http://localhost:8000, see package.json "proxy"
```

## Notes & next steps

- CORS is wide open (`allow_origins=["*"]`) for easy local development —
  restrict this before deploying publicly.
- There's no auth layer; adding an admin login before exposing the
  create/update/delete burger endpoints publicly is recommended.
- Order status (`pending → preparing → out_for_delivery → delivered`) can be
  updated via the API for a future kitchen/admin dashboard.
- The MySQL data persists in the `burger_mysql_data` Docker volume across
  restarts.
# burger_app
