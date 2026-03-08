from app.models.audit_log import AuditLog
from app.models.user import User


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_audit_logs_written_for_register_login_project_and_billing(client, db_session):
    reg = client.post("/api/v1/auth/register", json={"email": "audit@example.com", "password": "password123"})
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(User).filter(User.email == "audit@example.com").first()
    assert user is not None

    login = client.post("/api/v1/auth/login-json", json={"email": "audit@example.com", "password": "password123"})
    assert login.status_code == 200

    create = client.post("/api/v1/projects", json={"name": "Audit Project"}, headers=headers)
    assert create.status_code == 200

    checkout = client.post("/api/v1/billing/checkout/pro", headers=headers)
    assert checkout.status_code == 200

    webhook = client.post("/api/v1/billing/mock-webhook/success", headers=headers)
    assert webhook.status_code == 200

    actions = [row.action for row in db_session.query(AuditLog).filter(AuditLog.actor_user_id == user.id).all()]

    assert "register" in actions
    assert "login" in actions
    assert "create" in actions
    assert "checkout_start" in actions
    assert "webhook_success" in actions
