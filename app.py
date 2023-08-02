from flask import Flask, jsonify, request
from models import *
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


@app.route("/room", methods=["POST"])
def add_room():
    name = request.json["name"]
    description = request.json["description"]
    capacity = request.json["capacity"]
    projector = request.json["projector"]
    conditioning = request.json["conditioning"]
    tv = request.json["tv"]
    ethernet = request.json["ethernet"]
    whiteboard = request.json["whiteboard"]
    wifi = request.json["wifi"]

    new_room = Room(name=name, description=description, projector=projector,
                    conditioning=conditioning, tv=tv, ethernet=ethernet, whiteboard=whiteboard, wifi=wifi)

    db.session.add(new_room)
    db.session.commit()

    return jsonify("dziala")

@app.route('/')
def index():
    return jsonify("Hello World!")


@app.route("/rooms")
def get_rooms():
    rooms = db.session.execute(db.select(Room)).all()
    data = []
    for room in rooms:
        temp = {
            "id": room[0].id,
            "name": room[0].name,
            "description": room[0].description,
            # "capacity": room.capacity,
            "projector": room[0].projector,
            "conditioning": room[0].conditioning,
            "tv": room[0].tv,
            "ethernet": room[0].ethernet,
            "wifi": room[0].wifi,
            "whiteboard": room[0].whiteboard
        }
        data.append(temp)
    return jsonify(data)


app.run()
