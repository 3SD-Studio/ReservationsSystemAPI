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

    new_room = Room(name=name, description=description, capacity=capacity, projector=projector,
                    conditioning=conditioning, tv=tv, ethernet=ethernet, whiteboard=whiteboard, wifi=wifi)

    db.session.add(new_room)
    db.session.commit()

    return jsonify("The room has been added!")

@app.route('/')
def index():
    return jsonify("Hello World!")


@app.route("/rooms")
def get_rooms():
    rooms = db.session.execute(db.select(Room)).all()
    return jsonify([room[0].obj_to_dict() for room in rooms])


app.run()
