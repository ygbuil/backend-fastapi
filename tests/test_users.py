def test_create_user(client):
    response = client.post('/users', json={
        'username': 'test_user', 'password': '123',
        'location': 'test_location', 'lat': 12.58658855, 'lon': 54.39338383,
        'color': 'test_color'
    })

    assert response.status_code == 201


def test_get_acess_token(client, test_user_1):
    response = client.post('/token', data={
        'username': test_user_1['username'],
        'password': test_user_1['password'],
        'grant_type': 'password'
    })
    
    assert response.status_code == 200


def test_update_user(client, test_user_1, test_token_1):
    client.headers = {
        **client.headers, 'Authorization': f'Bearer {test_token_1}'
    }

    response = client.put(
        f"/users/{test_user_1['user_id']}", json={
            'user_id': test_user_1['user_id'], 'color': 'red'
        }
    )
    
    assert response.json()['color'] == 'red'
    assert response.status_code == 200


def test_update_user_unauthorized(client, test_user_1, test_token_2):
    client.headers = {
        **client.headers, 'Authorization': f'Bearer {test_token_2}'
    }

    response = client.put(
        f"/users/{test_user_1['user_id']}", json={
            'user_id': test_user_1['user_id'], 'color': 'red'
        }
    )

    response = client.put(
        f"/users/{test_user_1['user_id']}", json={
            'user_id': test_user_1['user_id'], 'color': 'red'
        }
    )
    
    assert response.status_code == 403


def test_delete_user(client, test_user_1, test_token_1):
    client.headers = {
        **client.headers, 'Authorization': f'Bearer {test_token_1}'
    }

    response = client.delete(f"/users/{test_user_1['user_id']}")

    assert response.status_code == 200


def test_delete_user_unauthorized(client, test_user_1, test_token_2):
    client.headers = {
        **client.headers, 'Authorization': f'Bearer {test_token_2}'
    }

    response = client.delete(f"/users/{test_user_1['user_id']}")

    assert response.status_code == 403
