
# Project Management SaaS

A **full‑stack Project Management SaaS platform** built with:

- **FastAPI Backend**
- **React + Vite Frontend**
- **MySQL Database**
- **JWT Authentication**
- **Stripe‑ready Billing Architecture**
- **Docker for database setup**
- **Automated Backend Testing**

The application demonstrates **production‑style architecture, clean code organization, and scalable SaaS design**.

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy ORM
- MySQL 8
- Alembic (database migrations)
- JWT Authentication
- Pytest (automated testing)
- Mock Stripe / Stripe-ready billing architecture

## Frontend

- React 18
- Vite
- TailwindCSS
- React Router
- Axios
- Stripe.js (frontend library)
- Node.js

---

# Architecture Overview

Client (React / Swagger)  
↓  
FastAPI Routers (API Layer)  
↓  
Service Layer (Business Logic)  
↓  
SQLAlchemy Models  
↓  
MySQL Database

---

# Project Structure

```text
project-management-saas
│
├── README.md
├── .gitignore
│
├── backend
│   │
│   ├── app
│   │   │
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── routers
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── billing.py
│   │   │   └── admin.py
│   │   │
│   │   ├── services
│   │   │   ├── audit_service.py
│   │   │   ├── subscription_service.py
│   │   │   ├── mock_stripe_service.py
│   │   │   └── stripe_service.py
│   │   │
│   │   ├── models
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── subscription.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas
│   │   │   ├── auth.py
│   │   │   ├── project.py
│   │   │   ├── subscription.py
│   │   │   └── admin.py
│   │   │
│   │   ├── dependencies
│   │   │   ├── auth.py
│   │   │   └── roles.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic
│   │   ├── env.py
│   │   └── versions
│   │
│   ├── tests
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   ├── test_billing.py
│   │   ├── test_admin.py
│   │   └── test_health_and_audit.py
│   │
│   ├── requirements.txt
│   └── alembic.ini
│
└── frontend
    │
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── .env
    │
    └── src
        │
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        │
        ├── api
        │   └── client.js
        │
        ├── components
        │   ├── Card.jsx
        │   └── Table.jsx
        │
        ├── guards
        │   ├── RequireAuth.jsx
        │   └── RequireAdmin.jsx
        │
        ├── layouts
        │   ├── AppLayout.jsx
        │   └── AdminLayout.jsx
        │
        └── pages
            ├── Login.jsx
            ├── Register.jsx
            ├── Projects.jsx
            ├── Billing.jsx
            ├── AdminUsers.jsx
            ├── AdminSubscriptions.jsx
            ├── AdminMapping.jsx
            ├── MockCheckout.jsx
            └── MockPortal.jsx
```

---

# Authentication

Supported authentication flows:

- User registration
- JWT login
- OAuth2 form login (Swagger)
- JSON login endpoint (React frontend)
- Role‑based access control

Endpoints

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/login-json
```

---

# Project Management Features

Users can:

- Create projects
- View their projects
- Delete projects
- Manage project data

Endpoints

```
POST /api/v1/projects
GET  /api/v1/projects
```

---

# Subscription System

The platform supports **SaaS subscription billing**.

Users can:

- Upgrade to Pro
- Cancel subscription
- View billing status

Endpoints

```
GET  /api/v1/billing/me
POST /api/v1/billing/checkout/pro
POST /api/v1/billing/mock-webhook/success
POST /api/v1/billing/mock-webhook/cancel
```

---

# Admin APIs

Admins can monitor platform activity.

Capabilities

- View users
- View subscriptions
- View user‑subscription mapping

Endpoints

```
GET /api/v1/admin/users
GET /api/v1/admin/subscriptions
GET /api/v1/admin/mapping
```

---

# Audit Logging

All major actions are logged:

- user registration
- login
- project creation
- subscription checkout
- subscription update

Audit data stored in **audit_logs table**.

---

# Running MySQL with Docker

Pull MySQL image

```bash
docker pull mysql:8
```

Run container

```bash
docker run -d --name pm_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=pm_saas mysql:8
```

Verify container

```bash
docker ps
```

Connect to MySQL

```bash
docker exec -it pm_mysql mysql -uroot -proot
```

---

# Backend Installation

Clone repository

```bash
git clone <repo-url>
cd project-management-saas/backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```
DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/pm_saas

JWT_SECRET_KEY=your_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60

SEED_ADMIN=true
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin1234
```

Run migrations

```bash
alembic upgrade head
```

Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger docs

```
http://127.0.0.1:8000/docs
```

---

# Frontend Installation

Navigate to frontend folder

```bash
cd ../frontend
```

Install dependencies

```bash
npm install
```

Create `.env`

```
VITE_API_BASE=http://127.0.0.1:8000/api/v1
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_example
```

Intall tailwind CSS

    npm install tailwindcss @tailwindcss/vite

Installing react-router, axios, stripe

```bash
    npm install react-router-dom axios @stripe/stripe-js @stripe/react-stripe-js
```

Modify vite.config.js

    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react-swc'
    import tailwindcss from '@tailwindcss/vite'

    // https://vite.dev/config/
    export default defineConfig({
      plugins: [react(), tailwindcss()],
    })

Run development server

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# Running Backend Tests

Run tests

```bash
pytest -q
```

Tests cover:

- Authentication
- Projects
- Billing
- Admin APIs
- Audit logging
- Health endpoint

---

# Security Features

- JWT authentication
- Password hashing with bcrypt
- Role‑based authorization
- Input validation with Pydantic

---

# Performance Considerations

- Indexed database columns
- Optimized queries

---
