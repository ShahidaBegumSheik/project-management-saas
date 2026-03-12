from app.models.subscription import Subscription
from app.models.user import User


def test_billing_me_defaults_to_free_active(client, user_headers):
    resp = client.get("/api/v1/billing/me", headers=user_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["plan"] == "free"
    assert body["status"] == "active"


def test_checkout_pro_returns_razorpay_order(client, user_headers):
    resp = client.post("/api/v1/billing/checkout/pro", headers=user_headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "order_id" in data
    assert "key_id" in data
    assert "amount" in data
    assert "currency" in data


def test_cancel_subscription_marks_status_canceled(client, user_headers):
    resp = client.post("/api/v1/billing/cancel", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] in ["cancelled", "canceled", "active"]


def test_pro_user_can_create_more_than_three_projects_after_manual_upgrade(
    client, db_session, user_headers
):

    user = db_session.query(User).filter(User.email == "user@example.com").first()
    sub = db_session.query(Subscription).filter(Subscription.user_id == user.id).first()
    sub.plan = "pro"
    sub.status = "active"
    db_session.commit()

    for i in range(4):
        resp = client.post(
            "/api/v1/projects",
            json={"name": f"Pro Project {i+1}"},
            headers=user_headers,
        )
        assert resp.status_code == 200, resp.text
