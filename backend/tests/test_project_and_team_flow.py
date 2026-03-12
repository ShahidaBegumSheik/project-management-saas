from app.models.notification import Notification
from app.models.team_invitation import TeamInvitation
from app.models.user import User, UserRole


def _register_and_verify(client, email: str, password: str = "password123"):
    res = client.post(
        "/api/v1/auth/register", json={"email": email, "password": password}
    )
    assert res.status_code == 200, res.text
    token = res.json().get("verification_token")
    if token:
        verify = client.get(f"/api/v1/auth/verify-email?token={token}")
        assert verify.status_code == 200, verify.text
    login = client.post(
        "/api/v1/auth/login", data={"username": email, "password": password}
    )
    assert login.status_code == 200, login.text
    access = login.json()["access_token"]
    return {"Authorization": f"Bearer {access}"}


def test_user_can_create_project_without_team(client):
    headers = _register_and_verify(client, "creator@example.com")
    resp = client.post(
        "/api/v1/projects",
        json={"name": "Solo Project", "description": "demo"},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["name"] == "Solo Project"
    assert body["team_id"] is None


def test_admin_cannot_create_project(client, db_session):
    _register_and_verify(client, "admin@gmail.com", "admin1234")
    admin = db_session.query(User).filter(User.email == "admin@gmail.com").first()
    admin.role = UserRole.admin
    db_session.commit()
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@gmail.com", "password": "admin1234"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    resp = client.post("/api/v1/projects", json={"name": "Blocked"}, headers=headers)
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Only users can perform this action"


def test_team_invitation_accept_flow_creates_membership_and_notification(
    client, db_session
):
    owner_headers = _register_and_verify(client, "owner2@example.com")
    member_headers = _register_and_verify(client, "member2@example.com")

    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Team Project", "description": "Project for team"},
        headers=owner_headers,
    )
    assert project_resp.status_code == 200, project_resp.text
    project_id = project_resp.json()["id"]

    create_team = client.post(
        "/api/v1/teams",
        json={"name": "Alpha", "description": "Team Alpha", "project_id": project_id},
        headers=owner_headers,
    )
    assert create_team.status_code == 200, create_team.text
    team_id = create_team.json()["id"]
    invite = client.post(
        f"/api/v1/teams/{team_id}/invite",
        json={"email": "member2@example.com"},
        headers=owner_headers,
    )
    assert invite.status_code == 200, invite.text
    token = (
        db_session.query(TeamInvitation)
        .filter(TeamInvitation.team_id == team_id)
        .first()
        .token
    )
    accept = client.post(
        f"/api/v1/teams/invitations/{token}",
        json={"action": "accept"},
        headers=member_headers,
    )
    assert accept.status_code == 200, accept.text
    notifications = db_session.query(Notification).all()
    assert any(n.title == "Invitation accepted" for n in notifications)
