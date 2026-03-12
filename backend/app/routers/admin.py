from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.roles import require_admin
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.admin import (AdminSubscriptionOut, AdminUserOut,
                               UserSubscriptionMapOut)
from app.schemas.notification import AdminNotificationCreate
from app.services.notification_service import create_notification

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AdminUserOut])
def all_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    stmt = select(User).order_by(User.created_at.desc())
    return list(db.scalars(stmt).all())


@router.get("/subscriptions", response_model=list[AdminSubscriptionOut])
def all_subscriptions(db: Session = Depends(get_db), admin=Depends(require_admin)):
    stmt = select(Subscription).order_by(Subscription.updated_at.desc())
    return list(db.scalars(stmt).all())


@router.get("/user-subscriptions", response_model=list[UserSubscriptionMapOut])
def user_subscription_map(db: Session = Depends(get_db), admin=Depends(require_admin)):
    rows = db.execute(
        select(User.id, User.email, Subscription.plan, Subscription.status)
        .join(Subscription, Subscription.user_id == User.id)
        .order_by(User.id.asc())
    ).all()
    return [
        {"user_id": r[0], "email": r[1], "plan": r[2], "status": r[3]} for r in rows
    ]


@router.post("/notifications")
def send_system_notification(
    payload: AdminNotificationCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    if payload.user_id:
        create_notification(
            db, payload.user_id, payload.title, payload.message, payload.type
        )
    else:
        for (user_id,) in db.query(User.id).all():
            create_notification(
                db, user_id, payload.title, payload.message, payload.type
            )
    db.commit()
    return {"message": "Notification sent"}
