def _create(client, email="jane@example.com", full_name="Jane Doe"):
    return client.post("/users", json={"email": email, "full_name": full_name})


def test_create_and_get_user(client):
    r = _create(client)
    assert r.status_code == 201
    user = r.json()
    assert user["email"] == "jane@example.com"
    assert user["is_active"] is True

    assert client.get(f"/users/{user['id']}").json() == user


def test_duplicate_email_conflict(client):
    _create(client)
    assert _create(client).status_code == 409


def test_invalid_email_rejected(client):
    assert _create(client, email="not-an-email").status_code == 422


def test_list_users(client):
    _create(client, "a@example.com")
    _create(client, "b@example.com")
    emails = [u["email"] for u in client.get("/users").json()]
    assert emails == ["a@example.com", "b@example.com"]
    assert len(client.get("/users?limit=1").json()) == 1


def test_update_user(client):
    user_id = _create(client).json()["id"]
    r = client.patch(f"/users/{user_id}", json={"full_name": "Jane Smith", "is_active": False})
    assert r.status_code == 200
    assert r.json()["full_name"] == "Jane Smith"
    assert r.json()["is_active"] is False
    assert r.json()["email"] == "jane@example.com"


def test_update_to_taken_email_conflict(client):
    _create(client, "a@example.com")
    user_id = _create(client, "b@example.com").json()["id"]
    assert client.patch(f"/users/{user_id}", json={"email": "a@example.com"}).status_code == 409


def test_delete_user(client):
    user_id = _create(client).json()["id"]
    assert client.delete(f"/users/{user_id}").status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404
    assert client.delete(f"/users/{user_id}").status_code == 404
