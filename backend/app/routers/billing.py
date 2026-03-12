from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_end_user
from app.models import Subscription
from app.schemas.subscription import (RazorpayOrderOut, SubscriptionOut,
                                      VerifyPaymentIn)
from app.services.audit_service import log_action
from app.services.email_service import (send_payment_failed_email,
                                        send_subscription_cancelled_email,
                                        send_subscription_email)
from app.services.invoice_service import generate_invoice
from app.services.notification_service import create_notification
from app.services.razorpay_service import (create_order,
                                           verify_payment_signature,
                                           verify_webhook_signature)
from app.services.subscription_service import (get_or_create_subscription,
                                               touch_subscription)

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/me", response_model=SubscriptionOut)
def billing_me(db: Session = Depends(get_db), user=Depends(require_end_user)):
    sub = get_or_create_subscription(db, user.id)
    db.commit()
    db.refresh(sub)
    return sub


@router.post("/checkout/pro", response_model=RazorpayOrderOut)
def checkout_pro(db: Session = Depends(get_db), user=Depends(require_end_user)):
    sub = get_or_create_subscription(db, user.id)
    order = create_order()
    sub.provider = "razorpay"
    sub.razorpay_order_id = order["id"]
    touch_subscription(sub)
    log_action(
        db,
        user.id,
        "checkout_start",
        "subscription",
        str(sub.id),
        {"order_id": order["id"]},
    )
    db.commit()
    return RazorpayOrderOut(
        order_id=order["id"],
        key_id=__import__(
            "app.core.config", fromlist=["settings"]
        ).settings.razorpay_key_id,
        amount=order["amount"],
        currency=order["currency"],
        company_name=__import__(
            "app.core.config", fromlist=["settings"]
        ).settings.razorpay_company_name,
        description=__import__(
            "app.core.config", fromlist=["settings"]
        ).settings.razorpay_company_description,
    )


@router.post("/verify-payment")
def verify_payment(
    payload: VerifyPaymentIn,
    db: Session = Depends(get_db),
    user=Depends(require_end_user),
):
    sub = get_or_create_subscription(db, user.id)
    if sub.razorpay_order_id != payload.razorpay_order_id:
        raise HTTPException(status_code=400, detail="Order mismatch")
    if not verify_payment_signature(
        payload.razorpay_order_id,
        payload.razorpay_payment_id,
        payload.razorpay_signature,
    ):
        sub.status = "payment_failed"
        touch_subscription(sub)
        db.commit()
        try:
            send_payment_failed_email(user.email, "Signature verification failed")
        except Exception as e:
            print(f"Failure email sending failed: {e}")
        create_notification(
            db,
            user.id,
            "Payment failed",
            "Your Razorpay payment could not be verified.",
            "billing",
        )
        db.commit()
        raise HTTPException(status_code=400, detail="Payment verification failed")

    sub.plan = "pro"
    sub.status = "active"
    sub.razorpay_payment_id = payload.razorpay_payment_id
    touch_subscription(sub)

    invoice = generate_invoice(user, sub)
    try:
        send_subscription_email(user.email, invoice)
    except Exception as e:
        print(f"Email sending failed: {e}")

    create_notification(
        db,
        user.id,
        "Subscription upgraded",
        "Your subscription is now on the Pro plan.",
        "billing",
    )
    log_action(
        db,
        user.id,
        "payment_verified",
        "subscription",
        str(sub.id),
        {"payment_id": payload.razorpay_payment_id},
    )
    db.commit()
    return {"status": "success", "message": "Payment verified and Pro plan activated"}


@router.post("/cancel")
def cancel_subscription(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    sub.plan = "free"
    sub.status = "cancelled"

    try:
        send_subscription_cancelled_email(user.email)
    except Exception as e:
        print(f"Cancellation email sending failed: {e}")

    create_notification(
        db,
        user.id,
        "Subscription cancelled",
        "Your plan has been downgraded to Free plan.",
        "billing",
    )
    log_action(
        db,
        user.id,
        "subscription_cancelled",
        "subscription",
        str(sub.id),
        {"plan": sub.plan},
    )
    db.commit()
    return {"status": "cancelled"}


@router.post("/razorpay/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing webhook signature")
    try:
        ok = verify_webhook_signature(body, signature)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook verification failed: {e}")
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    event = await request.json()
    if event.get("event") == "payment.captured":
        payment = event.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = payment.get("order_id")
        payment_id = payment.get("id")
        if order_id:
            from app.models.subscription import Subscription

            sub = (
                db.query(Subscription)
                .filter(Subscription.razorpay_order_id == order_id)
                .first()
            )
            if sub:
                sub.plan = "pro"
                sub.status = "active"
                sub.razorpay_payment_id = payment_id
                sub.updated_at = datetime.now(timezone.utc)
                create_notification(
                    db,
                    sub.user_id,
                    "Subscription upgraded",
                    "Your Razorpay webhook confirmed the payment.",
                    "billing",
                )
                db.commit()
    return {"received": True}
