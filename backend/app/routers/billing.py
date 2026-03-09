from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.subscription_service import get_or_create_subscription
from app.services.audit_service import log_action
from app.services import stripe_mock
from app.services.email_service import (
    send_subscription_email, 
    send_payment_failed_email,
    send_subscription_cancelled_email,
)
from app.services.invoice_service import generate_invoice
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

"""@router.post("/portal")
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
"""
@router.post("/mock-webhook/success")
def mock_webhook_success(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = get_or_create_subscription(db, user.id)

    sub.plan = "pro"
    sub.status = "active"

    db.commit()
    db.refresh(sub)

    invoice = generate_invoice(user, sub)
    try:
        send_subscription_email(user.email,invoice )
    except Exception as e:
        print(f"Email sending failed: {e}")

    log_action(db, user.id, "webhook_success", "subscription", str(sub.id), {"plan": "pro"})

    db.commit()

    return {"status": "success", "message": "Subscription upgraded to Pro successfully"}

@router.post("/mock-webhook/failure")
def mock_failure(user=Depends(get_current_user), db: Session = Depends(get_db)):
    
    subscription = get_or_create_subscription(db, user.id)

    subscription.plan = "free"
    subscription.status = "payment_failed"

    db.commit()
    db.refresh(subscription)

    try:
        send_payment_failed_email(user.email, reason="Insufficient funds or payment authorization failed")
    except Exception as e:
        print(f"Failure email sending failed: {e}")

    log_action(db, user.id, "webhook_failed", "subscription", str(subscription.id),
               {"reason": "Insufficient finds or payment authorization failed"},)
    
    db.commit()

    return {
        "status": "failure",
        "message": "Payment failed. Subscription not activated"
    }
    

@router.post("/mock-webhook/downgrade")
def mock_webhook_downgrade(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription = get_or_create_subscription(db, current_user.id)

    if subscription.plan != "pro":
        raise HTTPException(
            status_code=400,
            detail="Only Pro subscriptions can be cancelled"
        )

    subscription.plan = "free"
    subscription.status = "active"

    db.commit()
    db.refresh(subscription)

    try:
        send_subscription_cancelled_email(current_user.email)
    except Exception as e:
        print(f"Cancellation email sending failed: {e}")

    log_action(
        db,
        current_user.id,
        "subscription_cancelled",
        "subscription",
        str(subscription.id),
        {"new_plan": "free"},
    )
    db.commit()

    return {
        "status": "downgraded",
        "message": "Subscription cancelled and downgraded to Free plan"
    }
