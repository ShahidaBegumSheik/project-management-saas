from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.dependencies.roles import require_admin
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.admin import AdminUserOut, AdminSubscriptionOut, UserSubscriptionMapOut

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[AdminUserOut])
def all_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
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
    return [{"user_id": r[0], "email": r[1], "plan": r[2], "status": r[3]} for r in rows]
