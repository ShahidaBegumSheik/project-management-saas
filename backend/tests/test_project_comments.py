from app.models.team_invitation import TeamInvitation


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


def test_team_member_can_add_and_list_project_comments(client, db_session):
    owner_headers = _register_and_verify(client, "comment-owner@example.com")
    member_headers = _register_and_verify(client, "comment-member@example.com")

    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Project with comments", "description": "Comments in Project"},
        headers=owner_headers,
    )
    assert project_resp.status_code == 200, project_resp.text
    project_id = project_resp.json()["id"]

    create_team = client.post(
        "/api/v1/teams",
        json={"name": "Team A", "description": "Team", "project_id": project_id},
        headers=owner_headers,
    )
    team_id = create_team.json()["id"]

    invite = client.post(
        f"/api/v1/teams/{team_id}/invite",
        json={"email": "comment-member@example.com"},
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

    create_comment = client.post(
        f"/api/v1/projects/{project_id}/comments",
        json={"content": "I have reviewed the latest build."},
        headers=member_headers,
    )
    assert create_comment.status_code == 200, create_comment.text
    assert create_comment.json()["author_email"] == "comment-member@example.com"

    list_comments = client.get(
        f"/api/v1/projects/{project_id}/comments", headers=owner_headers
    )
    assert list_comments.status_code == 200, list_comments.text
    assert len(list_comments.json()) == 1
    assert list_comments.json()[0]["content"] == "I have reviewed the latest build."


def test_only_comment_owner_can_delete_comment(client):
    owner_headers = _register_and_verify(client, "comment-owner2@example.com")
    member_headers = _register_and_verify(client, "comment-member2@example.com")

    project_resp = client.post(
        "/api/v1/projects",
        json={"name": "Own Comment Project"},
        headers=owner_headers,
    )
    project_id = project_resp.json()["id"]

    owner_comment = client.post(
        f"/api/v1/projects/{project_id}/comments",
        json={"content": "Owner comment"},
        headers=owner_headers,
    )
    comment_id = owner_comment.json()["id"]

    forbidden = client.delete(
        f"/api/v1/projects/{project_id}/comments/{comment_id}",
        headers=member_headers,
    )
    assert forbidden.status_code in [403, 404]

    delete_ok = client.delete(
        f"/api/v1/projects/{project_id}/comments/{comment_id}",
        headers=owner_headers,
    )
    assert delete_ok.status_code == 200
    assert delete_ok.json()["deleted"] is True