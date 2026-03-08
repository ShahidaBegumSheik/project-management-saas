from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, projects, billing, admin

app = FastAPI(
    title="Project Management SaaS",
    version="1.0.0",
    description="""
This API supports:

### User Features
- Authnetication
- Project Management
- Subscription Billing

### Admin Features
- User Monitoring
- Subscription Monitoring

### Technology Stack

Backend
- FastAPI
- SQLAlchemy
- MySQL 8+
- Alembic migrations
- JWT authentication
- Stripe (subscriptions + webhooks)

Paytment
- Simulated Stripe (Simulated Subscription System)
""",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
