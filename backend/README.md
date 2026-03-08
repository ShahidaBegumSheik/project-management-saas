# Project Management SaaS (FastAPI + React + Stripe)

This repository implements the assignment requirements:
- Auth (register/login) with JWT
- User vs Admin panels
- Project CRUD with **Free plan = max 3 projects** (server-side enforcement)
- Stripe Checkout for Pro subscriptions + webhook sync
- Admin views for users/subscriptions/mapping

## Backend Setup (FastAPI + MySQL + Alembic)

### 1) Prereqs
- Python 3.10+
- Docker (recommended) OR MySQL 8 installed locally
- Stripe account with:
  - a recurring Price for your Pro plan
  - a webhook endpoint for `POST /api/v1/webhooks/stripe`

### 2) Start MySQL (Docker)
```bash
cd backend
docker compose up -d
```

### 3) Create virtualenv + install deps
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# mac/linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4) Configure env
```bash
cp .env.example .env
# edit DATABASE_URL / JWT_SECRET_KEY / STRIPE keys
```

### 5) Run migrations
```bash
alembic upgrade head
```

### 6) Run API
```bash
uvicorn app.main:app --reload
```

Open:
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Stripe Configuration Notes

### Checkout
`POST /api/v1/billing/checkout/pro` creates a Stripe Checkout Session in **subscription mode**.

### Webhook
Create a Stripe webhook endpoint pointing to:
`http://localhost:8000/api/v1/webhooks/stripe`

Set the environment variable:
- `STRIPE_WEBHOOK_SECRET=whsec_...`

Enable at least:
- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

## Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

App runs at: http://localhost:5173

## Tests (backend)
```bash
cd backend
pytest -q
```

## Architecture / Tradeoffs (brief)
- Tests use SQLite in-memory for speed; production uses MySQL per assignment.
- Subscription enforcement is **server-side**: non-active subscriptions are treated as Free.
- Stripe webhook handler covers the minimum event types to sync subscription status.
