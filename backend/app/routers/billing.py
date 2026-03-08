from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.subscription import Subscription
from app.services.subscription_service import get_or_create_subscription
from app.services.audit_service import log_action
from app.services import stripe_mock
from app.schemas.subscription import SubscriptionOut

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/me", response_model=SubscriptionOut)
def billing_me(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = get_or_create_subscription(db, user.id)
    db.commit()
    return SubscriptionOut(
        plan=sub.plan,
        status=sub.status,
        stripe_customer_id=sub.stripe_customer_id,
        stripe_subscription_id=sub.stripe_subscription_id,
    )

@router.post("/checkout/pro")
def checkout_pro(db: Session = Depends(get_db), user=Depends(get_current_user)):
    session = stripe_mock.create_checkout_session(user.id)
    log_action(db, user.id, "checkout_start", "subscription", str(user.id), {"session_id": session["id"]})
    db.commit()
    return {"url": session["url"], "session_id": session["id"]}

@router.post("/portal")
def portal(db: Session = Depends(get_db), user=Depends(get_current_user)):
    portal = stripe_mock.create_portal_session(user.id)
    return {"url": portal["url"]}

@router.post("/cancel")
def cancel_subscription(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = get_or_create_subscription(db, user.id)
    sub.status = "canceled"
    log_action(db, user.id, "cancel", "subscription", str(sub.id), {})
    db.commit()
    return {"status": sub.status}

@router.post("/mock-webhook/success")
def mock_webhook_success(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = get_or_create_subscription(db, user.id)
    sub.plan = "pro"
    sub.status = "active"
    log_action(db, user.id, "webhook_success", "subscription", str(sub.id), {"plan": "pro"})
    db.commit()
    return {"ok": True, "plan": sub.plan, "status": sub.status}

@router.post("/mock-webhook/downgrade")
def mock_webhook_downgrade(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = get_or_create_subscription(db, user.id)
    sub.plan = "free"
    sub.status = "active"
    log_action(db, user.id, "webhook_downgrade", "subscription", str(sub.id), {"plan": "free"})
    db.commit()
    return {"ok": True, "plan": sub.plan, "status": sub.status}
