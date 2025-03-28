"""Testing for experiences endpoints."""

from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

_NEW_RATING = 4


def test_create_experience(client: TestClient, test_token_1: str) -> None:
    """Test create experience."""
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


def test_update_experience(
    client: TestClient, test_experience_1: dict[str, Any], test_token_1: str
) -> None:
    """Test update experience."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.put(
        f"/experiences/{test_experience_1['experience_id']}",
        json={
            "experience_id": test_experience_1["experience_id"],
            "title": test_experience_1["title"],
            "description": test_experience_1["description"],
            "location": test_experience_1["location"],
            "lat": test_experience_1["lat"],
            "lon": test_experience_1["lon"],
            "rating": _NEW_RATING,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["rating"] == _NEW_RATING


def test_update_experience_unauthorized(
    client: TestClient,
    test_experience_1: dict[str, Any],
    test_token_2: str,
) -> None:
    """Test update experience with unauthorized user."""
    response = client.put(
        f"/experiences/{test_experience_1['experience_id']}",
        json={
            "experience_id": test_experience_1["experience_id"],
            "title": test_experience_1["title"],
            "description": test_experience_1["description"],
            "location": test_experience_1["location"],
            "lat": test_experience_1["lat"],
            "lon": test_experience_1["lon"],
            "rating": _NEW_RATING,
        },
        headers={"Authorization": f"Bearer {test_token_2}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_experience(
    client: TestClient, test_experience_1: dict[str, Any], test_token_1: str
) -> None:
    """Test delete experience."""
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token_1}"}

    response = client.delete(f"/experiences/{test_experience_1['experience_id']}")

    assert response.status_code == status.HTTP_200_OK


def test_delete_experience_unauthorized(
    client: TestClient,
    test_experience_1: dict[str, Any],
    test_token_2: str,
) -> None:
    """Test delete experience with unauthorized user."""
    response = client.delete(
        f"/experiences/{test_experience_1['experience_id']}",
        headers={"Authorization": f"Bearer {test_token_2}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
