def test_hello_world_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_hw_html_deve_retornar_h1_ola_mundo(client):
    response = client.get('/html')

    assert response.status_code == 200
    assert response.text == '<h1>Hello World!</h1>'


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'user_name': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'user_name': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'user_name': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'user_name': 'bob',
            'email': 'bob@example.com',
            'password': 'xpto1234',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'user_name': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_get_user_by_id(client):
    response = client.get(
        'users/1',
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'user_name': 'bob',
        'email': 'bob@example.com',
    }


def test_uptade_user_with_invalid_id(client):
    response = client.put(
        '/users/-1',
        json={
            'user_name': 'bob',
            'email': 'bob@example.com',
            'password': 'xpto1234',
        },
    )
    assert response.status_code == 404


def test_delete_user(client):
    response = client.delete(
        '/users/1',
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted.'}


def test_delete_user_with_invalid_id(client):
    response = client.delete(
        '/users/-1',
    )
    assert response.status_code == 404
