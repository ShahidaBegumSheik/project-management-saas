from app.models.audit_log import AuditLog
from app.models.user import User


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_audit_logs_written_for_register_login_project_and_billing(client, db_session):
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "audit@example.com", "password": "password123"},
    )
    assert reg.status_code == 200, reg.text

    verification_token = reg.json()["verification_token"]
    verify = client.get(f"/api/v1/auth/verify-email?token={verification_token}")
    assert verify.status_code == 200, verify.text

    login = client.post(
        "/api/v1/auth/login-json",
        json={"email": "audit@example.com", "password": "password123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]

    headers = {"AUthorization": f"Bearer {token}"}

    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Audit Project", "description": "Audit test project"},
        headers=headers,
    )
    assert project_resp.status_code == 200, project_resp.text

    cancel_resp = client.post("/api/v1/billing/cancel", headers=headers)
    assert cancel_resp.status_code == 200, cancel_resp.text

    user = db_session.query(User).filter(User.email == "audit@example.com").first()
    assert user is not None

    rows = db_session.query(AuditLog).filter(AuditLog.actor_user_id == user.id).all()
    actions = [row.action for row in rows]

    assert "register" in actions
    assert "login" in actions
    assert "create" in actions
    assert "subscription_cancelled" in actions
