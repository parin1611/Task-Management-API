def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    payload = {
        "name": "Alice",
        "email": "duplicate@example.com",
        "password": "password123",
    }

    first = client.post(
        "/auth/register",
        json=payload,
    )

    second = client.post(
        "/auth/register",
        json=payload,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_login(client):
    email = "login@example.com"
    password = "password123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20


def test_login_invalid_password(client):
    email = "invalid-password@example.com"

    client.post(
        "/auth/register",
        json={
            "name": "Invalid Password",
            "email": email,
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_jwt_authentication(client, auth_headers):
    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_task_access(client):
    response = client.get("/tasks")

    assert response.status_code == 401
