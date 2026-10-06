def create_task(client, auth_headers, title="Test Task"):
    return client.post(
        "/tasks",
        json={
            "title": title,
            "description": "Test description",
            "status": "pending",
        },
        headers=auth_headers,
    )


def test_create_task(client, auth_headers):
    response = create_task(
        client,
        auth_headers,
        title="My first task",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "My first task"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_by" in data
    assert "created_at" in data


def test_get_tasks(client, auth_headers):
    create_task(client, auth_headers, "Task 1")
    create_task(client, auth_headers, "Task 2")

    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 2
    assert {task["title"] for task in tasks} == {
        "Task 1",
        "Task 2",
    }


def test_get_single_task(client, auth_headers):
    create_response = create_task(
        client,
        auth_headers,
        "Single Task",
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Single Task"


def test_update_task(client, auth_headers):
    create_response = create_task(
        client,
        auth_headers,
        "Original title",
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "in_progress",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"
    assert data["status"] == "in_progress"


def test_delete_task(client, auth_headers):
    create_response = create_task(
        client,
        auth_headers,
        "Delete me",
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_task_ownership(client, auth_headers):
    create_response = create_task(
        client,
        auth_headers,
        "Private task",
    )

    task_id = create_response.json()["id"]

    # Register a different user.
    second_user = {
        "name": "Second User",
        "email": "second-user@example.com",
        "password": "password123",
    }

    register_response = client.post(
        "/auth/register",
        json=second_user,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": second_user["email"],
            "password": second_user["password"],
        },
    )

    second_headers = {
        "Authorization": (
            f"Bearer {login_response.json()['access_token']}"
        ),
    }

    # The second user cannot access the first user's task.
    response = client.get(
        f"/tasks/{task_id}",
        headers=second_headers,
    )

    assert response.status_code == 404

    # The second user cannot update it.
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Hijacked task",
        },
        headers=second_headers,
    )

    assert response.status_code == 404

    # The second user cannot delete it.
    response = client.delete(
        f"/tasks/{task_id}",
        headers=second_headers,
    )

    assert response.status_code == 404


def test_invalid_task_status(client, auth_headers):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid status task",
            "description": "Should fail",
            "status": "invalid_status",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_unauthorized_task_creation(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Unauthorized task",
            "description": "Should fail",
            "status": "pending",
        },
    )

    assert response.status_code == 401
