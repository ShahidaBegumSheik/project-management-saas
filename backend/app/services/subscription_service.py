from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.subscription import Subscription
from app.models.project import Project

FREE_PROJECT_LIMIT = 3

def get_or_create_subscription(db: Session, user_id: int) -> Subscription:
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not sub:
        sub = Subscription(user_id=user_id, plan="free", status="active")
        db.add(sub)
        db.flush()
    return sub

def enforce_project_limit(db: Session, user_id: int):
    sub = get_or_create_subscription(db, user_id)
    if sub.status != "active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Subscription inactive")

    if sub.plan == "free":
        count = db.query(func.count(Project.id)).filter(Project.owner_id == user_id).scalar() or 0
        if count >= FREE_PROJECT_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Free plan limit reached ({FREE_PROJECT_LIMIT}). Upgrade to Pro."
            )
