from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import (admin, analytics, auth, billing, notifications,
                         projects, teams)

app = FastAPI(
    title="Project Management SaaS",
    version="2.0.0",
    description="""
This API supports:

### User Features
- Authnetication and email verification
- Project Management
- Team collaboration
- In-app notification
- Activity tracking
- Razorpay billing

### Admin Features
- User Monitoring
- Subscription Monitoring
- Analytics dashboard
- System notifications

### Technology Stack

Backend
- FastAPI
- SQLAlchemy
- MySQL 8+
- Alembic migrations
- JWT authentication
- Stripe (subscriptions + webhooks)

Paytment
- Razorpay
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
app.include_router(teams.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
