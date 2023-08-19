def test_room_post(client, app):
    room_data = {
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

    user_data = {
        "email": "test@test.com",
        "firstName": "test",
        "lastName": "test",
        "password": "test123"
    }

    response = client.post("/register", json=user_data)

    token = response.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

    with app.app_context():
        response = client.post("/room", headers=headers, json=room_data)
    assert response.status_code == 401



