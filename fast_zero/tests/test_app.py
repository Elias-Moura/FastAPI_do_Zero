from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_hello_world_deve_retornar_200_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_hw_html_deve_retornar_h1_ola_mundo():
    client = TestClient(app)

    response = client.get('/html')

    assert response.status_code == 200
    assert response.text == '<h1>Hello World!</h1>'
