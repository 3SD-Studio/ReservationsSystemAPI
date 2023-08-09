from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from sqlalchemy.orm.exc import NoResultFound
from models import *
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


@app.route('/')
def index():
    return jsonify("Hello World!")


@app.route("/rooms")
def get_rooms():
    rooms = db.session.execute(db.select(Room)).all()
    return jsonify([room[0].obj_to_dict_short() for room in rooms])


@app.route("/room/<room_id>")
def get_room(room_id):
    try:
        room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
    except NoResultFound:
        abort(400, description='Invalid value for roomId parameter.')

    return jsonify(room.obj_to_dict())


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


@app.route("/events")
def get_events():
    events = db.session.execute(db.select(Event)).all()
    return jsonify([event[0].obj_to_dict() for event in events])


@app.route("/event/<event_id>")
def get_event(event_id):
    try:
        event = db.session.execute(db.select(Event).filter_by(id=event_id)).scalar_one()
    except NoResultFound:
        abort(400, description='Invalid value for eventId parameter.')

    return jsonify(event.obj_to_dict())


@app.route("/room/<room_id>/events")
def get_events_for_room(room_id):
    if len(request.args) <= 1:
        limit = request.args.get("limit", default=20, type=int)
        if 0 > limit or limit > 20:
            abort(400, description='Invalid value for limit parameter.')
        try:
            room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid value for roomId parameter.')

        events = room.events

        result = [event.obj_to_dict() for event in events if event.begin >= datetime.today()]
        sorted_result = sorted(result, key=lambda x: x['begin'])

        return jsonify(sorted_result[:limit])

    else:
        try:
            day = request.args.get("day", default=None, type=int)
            month = request.args.get("month", default=None, type=int)
            year = request.args.get("year", default=None, type=int)
            given_date = datetime(day=day, month=month, year=year)
        except ValueError:
            abort(400, description='Invalid value for date parameter.')

        try:
            room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid value for roomId parameter.')

        events = room.events

        result = [event.obj_to_dict() for event in events if event.begin.date() == given_date.date()]
        sorted_result = sorted(result, key=lambda x: x['begin'])

        return jsonify(sorted_result)


@app.route("/event", methods=["POST"])
def post_event():
    name = request.json["name"]
    description = request.json["description"]
    link = request.json["link"]
    begin = request.json["begin"]
    end = request.json["end"]
    ownerId = request.json["ownerId"]
    roomsId = request.json["roomsId"]

    new_event = Event(name=name, description=description, link=link,
                      begin=datetime.strptime(begin, DATE_FORMAT),
                      end=datetime.strptime(end, DATE_FORMAT), ownerId=ownerId)

    event_duration = new_event.end - new_event.begin
    if new_event.begin >= new_event.end:
        abort(400, description='Begin date is greater than end date.')
    if event_duration < timedelta(minutes=15):
        abort(400, description='Event duration cant be shorter than 15 minutes.')
    if new_event.begin.date() != new_event.end.date():
        abort(400, description='Begin and end date have to be the same.')
    if new_event.begin <= datetime.today():
        abort(400, description='Invalid begin date.')

    db.session.add(new_event)

    for roomId in roomsId:
        room = db.session.execute(db.select(Room).filter_by(id=roomId)).scalar_one()
        events = room.events
        for event in events:
            if ((new_event.begin > event.begin) and (new_event.begin < event.end)) \
                    or ((new_event.end > event.begin) and (new_event.end < event.end)):
                abort(400, description='Event date collides with an already existing event.')
        room.events.append(new_event)

    db.session.commit()

    return jsonify("The event has been added!")


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@app.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]
    user = User(email=email, password=password, role_id=1)
    login_user(user)
    return jsonify(user.to_json())


app.run()
