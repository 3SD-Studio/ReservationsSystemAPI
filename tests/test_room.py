def test_room_post(client, app):
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
    with app.app_context():
        response = client.post("/room", json=data)
    assert response.status == "200 OK"



