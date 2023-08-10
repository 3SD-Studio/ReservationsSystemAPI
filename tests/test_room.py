from flask import json
from project.models import User


def test_app(client):
    response = client.get("/")
    assert response.status == "200 OK"


def test_registration(client, app):
    data = {
        "email": "test@test.com",
        "firstName": "test",
        "lastName": "test",
        "password": "test"
    }

    response = client.post('/register', data=json.dumps(data))

    with app.app_context():
        assert response.status == "200 OK"
        assert User.query.count() == 1
        assert User.query.first().email == "contact3sdstudio@gmail.com"

