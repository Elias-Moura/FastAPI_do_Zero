from http import HTTPStatus

import pytest

from exceptions.UserAlreadyExists import UserAlreadyExists
from exceptions.UserNotFoundException import UserNotFoundException
from fast_zero.schemas import UserPublic


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
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_already_exists(client, user):
    with pytest.raises(UserAlreadyExists):
        response = client.post(
            '/users',
            json={
                'username': 'Teste',
                'email': 'teste@test.com',
                'password': 'testtest',
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'xpto1234',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_get_user_by_id(client, user):
    response = client.get(
        'users/1',
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@test.com',
    }


def test_get_user_by_id_not_found(client, user):
    with pytest.raises(UserNotFoundException):
        response = client.get(
            'users/10',
        )
        assert response.status_code == HTTPStatus.NOT_FOUND.value


def test_uptade_user_with_invalid_id(client):
    with pytest.raises(UserNotFoundException):
        response = client.put(
            '/users/-1',
            json={
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'xpto1234',
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND.value


def test_delete_user(client, user):
    response = client.delete(
        '/users/1',
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted.'}


def test_delete_user_with_invalid_id(client):
    with pytest.raises(UserNotFoundException):
        response = client.delete(
            '/users/-1',
        )
        assert response.status_code == 404


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}
