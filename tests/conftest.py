# libraries
import pytest
from datetime import timedelta
from fastapi.testclient import TestClient

# local libraries
from app import oauth2
from app.models import Base
from tests.database import app, engine


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)


@pytest.fixture
def test_user_1(client):
    response = client.post(
        '/users', json={
            'username': 'user_1', 'password': '123',
            'location': 'location_1', 'color': 'color_1'
        }
    )

    assert response.status_code == 201

    test_user_1 = response.json()
    test_user_1['password'] = '123'

    return test_user_1


@pytest.fixture
def test_user_2(client):
    response = client.post(
        '/users', json={
            'username': 'user_2', 'password': '123',
            'location': 'location_2', 'color': 'color_2'
        }
    )

    assert response.status_code == 201

    test_user_2 = response.json()
    test_user_2['password'] = '123'

    return test_user_2


@pytest.fixture
def test_token_1(test_user_1):
    token_1 = oauth2.create_token(
        username=test_user_1['username'], user_id=test_user_1['user_id'],
        color=test_user_1['color'], expiration_time=timedelta(minutes=30)
    )

    return token_1


@pytest.fixture
def test_token_2(test_user_2):
    token_2 = oauth2.create_token(
        username=test_user_2['username'], user_id=test_user_2['user_id'],
        color=test_user_2['color'], expiration_time=timedelta(minutes=30)
    )

    return token_2


@pytest.fixture
def test_experience_1(client, test_token_1):
    client.headers = {
        **client.headers, 'Authorization': f'Bearer {test_token_1}'
    }
    
    response = client.post(
        '/experiences', json={
            'title': 'Beach', 'description': 'A sunny day',
            'location': 'Costa Brava', 'rating': 5
        }
    )

    assert response.status_code == 201

    test_experience_1 = response.json()

    return test_experience_1
