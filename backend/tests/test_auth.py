from app.models.audit_log import AuditLog
from app.models.subscription import Subscription
from app.models.user import User


def test_register_creates_user_and_subscription(client, db_session):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "password123"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert body["verification_required"] is True
    assert "verification_token" in body

    user = db_session.query(User).filter(User.email == "alice@example.com").first()
    assert user is not None
    assert user.hashed_password != "password123"

    sub = db_session.query(Subscription).filter(Subscription.user_id == user.id).first()
    assert sub is not None
    assert sub.plan == "free"
    assert sub.status == "active"

    audit_rows = (
        db_session.query(AuditLog).filter(AuditLog.actor_user_id == user.id).all()
    )
    assert any(row.action == "register" for row in audit_rows)


def test_register_duplicate_email_fails(client):
    payload = {"email": "same@example.com", "password": "password123"}
    first = client.post("/api/v1/auth/register", json=payload)
    second = client.post("/api/v1/auth/register", json=payload)

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered"


def test_login_success_returns_token(client):
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "password123"},
    )
    token = reg.json()["verification_token"]
    verify = client.get(f"/api/v1/auth/verify-email?token={token}")
    assert verify.status_code == 200

    resp = client.post(
        "/api/v1/auth/login-json",
        json={"email": "bob@example.com", "password": "password123"},
    )
    assert resp.status_code == 200, resp.text
    assert "access_token" in resp.json()


def test_login_invalid_credentials_fails(client):
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "eve@example.com", "password": "password123"},
    )
    token = reg.json()["verification_token"]
    client.get(f"/api/v1/auth/verify-email?token={token}")

    resp = client.post(
        "/api/v1/auth/login-json",
        json={"email": "eve@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


def test_protected_endpoint_requires_token(client):
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 401


def test_login_success_returns_token_using_oauth_form(client):
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "form@example.com", "password": "password123"},
    )
    token = reg.json()["verification_token"]
    client.get(f"/api/v1/auth/verify-email?token={token}")

    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "form@example.com", "password": "password123"},
    )
    assert resp.status_code == 200, resp.text
    assert "access_token" in resp.json()
