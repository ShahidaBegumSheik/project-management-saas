from app.models.subscription import Subscription
from app.models.user import User


def test_billing_me_defaults_to_free_active(client, user_headers):
    resp = client.get("/api/v1/billing/me", headers=user_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["plan"] == "free"
    assert body["status"] == "active"
    assert body["stripe_customer_id"] is None
    assert body["stripe_subscription_id"] is None


def test_checkout_pro_returns_mock_checkout_url(client, user_headers):
    resp = client.post("/api/v1/billing/checkout/pro", headers=user_headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "url" in data
    assert "mock-checkout" in data["url"]
    assert "session_id" in data


def test_portal_returns_mock_portal_url(client, user_headers):
    resp = client.post("/api/v1/billing/portal", headers=user_headers)
    assert resp.status_code == 200
    assert "mock-portal" in resp.json()["url"]


def test_cancel_subscription_marks_status_canceled(client, user_headers):
    resp = client.post("/api/v1/billing/cancel", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "canceled"

    me = client.get("/api/v1/billing/me", headers=user_headers)
    assert me.status_code == 200
    assert me.json()["status"] == "canceled"


def test_mock_webhook_success_upgrades_to_pro(client, user_headers):
    resp = client.post("/api/v1/billing/mock-webhook/success", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["plan"] == "pro"
    assert resp.json()["status"] == "active"

    me = client.get("/api/v1/billing/me", headers=user_headers)
    assert me.json()["plan"] == "pro"


def test_mock_webhook_downgrade_returns_to_free(client, user_headers):
    client.post("/api/v1/billing/mock-webhook/success", headers=user_headers)

    resp = client.post("/api/v1/billing/mock-webhook/downgrade", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["plan"] == "free"
    assert resp.json()["status"] == "active"


def test_pro_user_can_create_more_than_three_projects(client, user_headers):
    up = client.post("/api/v1/billing/mock-webhook/success", headers=user_headers)
    assert up.status_code == 200

    for i in range(4):
        resp = client.post(
            "/api/v1/projects",
            json={"name": f"Pro Project {i+1}"},
            headers=user_headers,
        )
        assert resp.status_code == 200, resp.text
