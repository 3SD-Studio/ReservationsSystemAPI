from datetime import datetime

from flask import Flask, jsonify, request
from models import *
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

@app.route('/')
def index():
    return jsonify("Hello World!")


@app.route("/room/<room_id>")
def get_room(room_id):
    room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
    return jsonify(room.obj_to_dict())


@app.route("/rooms")
def get_rooms():
    rooms = db.session.execute(db.select(Room)).all()
    return jsonify([room[0].obj_to_dict() for room in rooms])


@app.route("/room", methods=["POST"])
def post_room():
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


@app.route("/event/<event_id>")
def get_event(event_id):
    event = db.session.execute(db.select(Event).filter_by(id=event_id)).scalar_one()
    return jsonify(event.obj_to_dict())


@app.route("/events")
def get_events():
    events = db.session.execute(db.select(Event)).all()
    return jsonify([event[0].obj_to_dict() for event in events])


@app.route("/event", methods=["POST"])
def post_event():
    name = request.json["name"]
    description = request.json["description"]
    link = request.json["link"]
    begin = request.json["begin"]
    end = request.json["end"]
    ownerId = request.json["ownerId"]

    new_event = Event(name=name, description=description, link=link,
                      begin=datetime.strptime(begin, DATE_FORMAT),
                      end=datetime.strptime(end, DATE_FORMAT), ownerId=ownerId)

    db.session.add(new_event)
    db.session.commit()

    return jsonify("The event has been added!")


app.run()
