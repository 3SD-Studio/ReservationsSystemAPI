from flask import json, jsonify
from project.models import User


def test_app(client):
    response = client.get("/")
    assert response.status == "200 OK"


def test_get(client):
    response = client.get("/events")
    assert response.status == "200 OK"


def test_room_post(client, app):
    with app.app_context():
        data = {
           "name": "Aaa",
           "description": "Sala konferencyjna 8",
           "capacity": 100,
           "projector": True,
           "conditioning": True,
           "tv": False,
           "ethernet": True,
           "wifi": True,
           "whiteboard": False
        }

    response = client.post("/room", json=data)
    assert response.status == "200 OK"


def test_registration(client, app):
    data = {
        "email": "test2@test.com",
        "firstName": "test",
        "lastName": "test",
        "password": "test"
    }

    response = client.post('/register', json=data)

    with app.app_context():
        assert response.status == "200 OK"
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"

