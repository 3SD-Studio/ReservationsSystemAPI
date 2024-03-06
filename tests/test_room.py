from project.functions import generate_token
from project.models import db, User


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
        admin = db.session.execute(db.select(User).filter_by(email="admin")).scalar_one()

    token = generate_token(admin.id)
    headers = {"Authorization": f"Bearer {token}"}
    print(admin.id)
    with app.app_context():
        response = client.post("/room", headers=headers, json=data)
    assert response.status_code == 200
