import os

# Set test configuration before importing the application.
# This keeps tests isolated from a developer's local .env/database.
os.environ["DATABASE_URL"] = "sqlite:///./test_task_management.db"
os.environ["SECRET_KEY"] = (
    "test-secret-key-for-pytest-only-"
    "do-not-use-in-production"
)
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.db.database import Base, engine
from app.main import app


TEST_DATABASE = Path("test_task_management.db")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def user_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    }


@pytest.fixture
def registered_user(client, user_data):
    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def auth_headers(client, user_data, registered_user):
    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }
