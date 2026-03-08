def test_non_admin_cannot_access_admin_routes(client, user_headers):
    endpoints = [
        "/api/v1/admin/users",
        "/api/v1/admin/subscriptions",
        "/api/v1/admin/user-subscriptions",
    ]
    for url in endpoints:
        resp = client.get(url, headers=user_headers)
        assert resp.status_code == 403
        assert resp.json()["detail"] == "Admin only"


def test_admin_can_list_users(client, admin_headers):
    resp = client.get("/api/v1/admin/users", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_admin_can_list_subscriptions(client, admin_headers):
    resp = client.get("/api/v1/admin/subscriptions", headers=admin_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_admin_can_view_user_subscription_mapping(client, admin_headers):
    resp = client.get("/api/v1/admin/user-subscriptions", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    row = data[0]
    assert "user_id" in row
    assert "email" in row
    assert "plan" in row
    assert "status" in row
