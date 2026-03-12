def test_list_projects_initially_empty(client, user_headers):
    resp = client.get("/api/v1/projects", headers=user_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_free_plan_allows_only_three_projects(client, user_headers):
    for i in range(3):
        resp = client.post(
            "/api/v1/projects",
            json={"name": f"Project {i+1}", "description": "demo"},
            headers=user_headers,
        )
        assert resp.status_code == 200, resp.text

    fourth = client.post(
        "/api/v1/projects",
        json={"name": "Project 4", "description": "demo"},
        headers=user_headers,
    )
    assert fourth.status_code == 403
    assert "Free plan limit reached" in fourth.json()["detail"]


def test_project_create_and_delete_flow(client, user_headers):
    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "Delete Me", "description": "temporary"},
        headers=user_headers,
    )
    assert create_resp.status_code == 200
    project_id = create_resp.json()["id"]

    list_resp = client.get("/api/v1/projects", headers=user_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    delete_resp = client.delete(f"/api/v1/projects/{project_id}", headers=user_headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["deleted"] is True

    list_again = client.get("/api/v1/projects", headers=user_headers)
    assert list_again.json() == []


def test_user_cannot_delete_other_users_project(client):
    def register_verify_login(email):
        reg = client.post(
            "/api/v1/auth/register", json={"email": email, "password": "password123"}
        )
        token = reg.json()["verification_token"]
        client.get(f"/api/v1/auth/verify-email?token={token}")
        login = client.post(
            "/api/v1/auth/login", data={"username": email, "password": "password123"}
        )
        access = login.json()["access_token"]
        return {"Authorization": f"Bearer {access}"}

    owner_headers = register_verify_login("owner@example.com")

    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "Owner Project"},
        headers=owner_headers,
    )
    project_id = create_resp.json()["id"]

    intruder_headers = register_verify_login("intruder@example.com")

    delete_resp = client.delete(
        f"/api/v1/projects/{project_id}", headers=intruder_headers
    )
    assert delete_resp.status_code == 200
    assert delete_resp.json()["deleted"] is False
