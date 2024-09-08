"""Testing for users endpoints."""

from fastapi import status
from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    """Test create user."""
    response = client.post(
        "/users",
        json={
            "username": "test_user",
            "password": "123",
            "location": "test_location",
            "lat": 12.58658855,
            "lon": 54.39338383,
            "color": "test_color",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_get_acess_token(client: TestClient, test_user_1: dict) -> None:
    """Test get access token."""
    response = client.post(
        "/token",
        data={
            "username": test_user_1["username"],
            "password": test_user_1["password"],
            "grant_type": "password",
        },
    )

    assert response.status_code == status.HTTP_200_OK


def test_update_user(client: TestClient, test_user_1: dict, test_token_1: str) -> None:
    """Test update user."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.put(
        f"/users/{test_user_1['user_id']}",
        json={
            "user_id": test_user_1["user_id"],
            "username": test_user_1["user_id"],
            "color": "red",
            "location": test_user_1["location"],
            "lat": test_user_1["lat"],
            "lon": test_user_1["lon"],
            "password": test_user_1["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["color"] == "red"


def test_update_user_unauthorized(client: TestClient, test_user_1: dict, test_token_2: str) -> None:
    """Test update user with unauthorized user."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_2}"}

    response = client.put(
        f"/users/{test_user_1['user_id']}",
        json={
            "user_id": test_user_1["user_id"],
            "username": test_user_1["user_id"],
            "color": "red",
            "location": test_user_1["location"],
            "lat": test_user_1["lat"],
            "lon": test_user_1["lon"],
            "password": test_user_1["password"],
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_user(client: TestClient, test_user_1: dict, test_token_1: str) -> None:
    """Test delete user."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.delete(f"/users/{test_user_1['user_id']}")

    assert response.status_code == status.HTTP_200_OK


def test_delete_user_unauthorized(client: TestClient, test_user_1: dict, test_token_2: str) -> None:
    """Test delete user with unauthorized user."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_2}"}

    response = client.delete(f"/users/{test_user_1['user_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
