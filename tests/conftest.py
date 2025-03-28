"""Fixtures for testing."""

from datetime import timedelta
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend_fastapi import endpoint_functions
from backend_fastapi.data import Base
from tests.database import app, engine


@pytest.fixture
def client() -> TestClient:
    """Client with test database."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return TestClient(app)


@pytest.fixture
def test_user_1(client: TestClient) -> dict[str, Any]:
    """Testing user number 1."""
    response = client.post(
        "/users",
        json={
            "username": "user_1",
            "password": "pw1",
            "location": "location_1",
            "lat": 12.58658855,
            "lon": 54.39338383,
            "color": "color_1",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    test_user_1 = response.json()
    test_user_1["password"] = "pw1"  # noqa: S105

    return test_user_1


@pytest.fixture
def test_user_2(client: TestClient) -> dict[str, Any]:
    """Testing user number 2."""
    response = client.post(
        "/users",
        json={
            "username": "user_2",
            "password": "pw2",
            "location": "location_2",
            "lat": 12.58658855,
            "lon": 54.39338383,
            "color": "color_2",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    test_user_2 = response.json()
    test_user_2["password"] = "pw2"  # noqa: S105

    return test_user_2


@pytest.fixture
def test_token_1(test_user_1: dict[str, Any]) -> str:
    """Token for testing user number 1."""
    return endpoint_functions.create_token(
        username=test_user_1["username"],
        user_id=test_user_1["user_id"],
        color=test_user_1["color"],
        expiration_time=timedelta(minutes=30),
    )


@pytest.fixture
def test_token_2(test_user_2: dict[str, Any]) -> str:
    """Token for testing user number 2."""
    return endpoint_functions.create_token(
        username=test_user_2["username"],
        user_id=test_user_2["user_id"],
        color=test_user_2["color"],
        expiration_time=timedelta(minutes=30),
    )


@pytest.fixture
def test_experience_1(client: TestClient, test_token_1: str) -> Any | dict[str, Any]:
    """Experience written by testing user number 1."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.post(
        "/experiences",
        json={
            "title": "Beach",
            "description": "A sunny day",
            "location": "Costa Brava",
            "lat": 12.58658855,
            "lon": 54.39338383,
            "rating": 5,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    return response.json()
