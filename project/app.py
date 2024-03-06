from flask_cors import CORS
from flask import Flask, jsonify, request, abort
from flask_login import LoginManager
from sqlalchemy.orm.exc import NoResultFound
from project.models import Room, Event, User, db
from project.functions import *

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def create_app(database_uri="sqlite:///database.db"):
    """
    Creates and configures the Flask application.

    Args:
        database_uri (str): The URI of the database. Defaults to "sqlite:///database.db".

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.secret_key = 'some key'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    db.init_app(app)
    CORS(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

    @app.route("/", methods=['GET'])
    def index():
        """
        Returns a JSON response with the message "Hello World!".
        """
        return jsonify("Hello World!")

    @app.route("/rooms", methods=['GET'])
    def get_rooms():
        """
        Retrieve all rooms from the database and return them as JSON.

        Returns:
            A JSON response containing a list of room objects.
        """
        rooms = db.session.execute(db.select(Room)).all()
        return jsonify([room[0].obj_to_dict_short() for room in rooms])

    @app.route("/room/<room_id>", methods=['GET'])
    def get_room(room_id):
        """
        Retrieve information about a specific room.

        Args:
            room_id (int): The ID of the room to retrieve.

        Returns:
            dict: A dictionary containing the room information.

        Raises:
            400: If the room ID is invalid.
        """
        try:
            room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid value for roomId parameter.')
        else:
            return jsonify(room.obj_to_dict())

    @app.route("/room", methods=["POST"])
    def post_room():
        """
        Add a new room to the system.

        This endpoint requires a valid token in the Authorization header with the format 'Bearer <token>'.
        Only users with the role of Editor or Admin can add a room.

        Request Body:
        - name: The name of the room (string)
        - description: The description of the room (string)
        - capacity: The capacity of the room (integer)
        - projector: Whether the room has a projector (boolean)
        - conditioning: Whether the room has air conditioning (boolean)
        - tv: Whether the room has a TV (boolean)
        - ethernet: Whether the room has Ethernet connection (boolean)
        - whiteboard: Whether the room has a whiteboard (boolean)
        - wifi: Whether the room has WiFi (boolean)

        Returns:
            A JSON response indicating the success of the operation.
        """
        token = request.headers.get('Authorization')
        if token is None or token[:7] != 'Bearer ':
            abort(401, description='Invalid token.')
        else:
            token = token[7:]

        userId = get_id_from_token(token)

        try:
            userRoleId = db.session.execute(db.select(User.role_id).filter_by(id=userId)).scalar_one()
        except NoResultFound:
            abort(401, description='Invalid token.')
        else:
            if userRoleId not in (2, 4):
                abort(401, description='Only Editor or Admin can add room')

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

    @app.route("/events", methods=['GET'])
    def get_events():
        """
        Retrieve all events from the database.

        Returns:
            A JSON response containing a list of event objects.
        """
        events = db.session.execute(db.select(Event)).all()
        return jsonify([event[0].obj_to_dict() for event in events])

    @app.route("/event/<event_id>", methods=['GET'])
    def get_event(event_id):
        """
        Retrieve an event by its ID.

        Args:
            event_id (int): The ID of the event to retrieve.

        Returns:
            dict: A dictionary representing the event object.

        Raises:
            400: If the event ID is invalid.
        """
        try:
            event = db.session.execute(db.select(Event).filter_by(id=event_id)).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid value for eventId parameter.')
        else:
            return jsonify(event.obj_to_dict())

    @app.route("/room/<room_id>/events", methods=['GET'])
    def get_events_for_room(room_id):
        """
        Retrieves events for a specific room based on the given parameters.

        Args:
            room_id (int): The ID of the room.

        Returns:
            A JSON response containing the events for the room.

        Raises:
            400: If there are invalid values for the parameters or if the room ID is invalid.
        """
        if len(request.args) <= 1:
            limit = request.args.get("limit", default=20, type=int)
            if 0 > limit or limit > 20:
                abort(400, description='Invalid value for limit parameter.')
            try:
                room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
            except NoResultFound:
                abort(400, description='Invalid value for roomId parameter.')
            else:
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
            else:
                try:
                    room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()
                except NoResultFound:
                    abort(400, description='Invalid value for roomId parameter.')
                else:
                    events = room.events

                    result = [event.obj_to_dict() for event in events if event.begin.date() == given_date.date()]
                    sorted_result = sorted(result, key=lambda x: x['begin'])

                    return jsonify(sorted_result)

    @app.route("/event", methods=["POST"])
    def post_event():
        """
        Create a new event.

        This function handles the POST request to create a new event in the reservations system.
        It retrieves the necessary data from the request JSON payload, validates the data,
        generates an edit password for the event, and saves the event to the database.

        Returns:
            A JSON response containing the ID of the newly created event and the edit password.

        Raises:
            400: If the provided data is invalid or the event date collides with an existing event.
            401: If the user is not authenticated or the provided token is invalid.
        """
        name = request.json["name"]
        description = request.json["description"]
        link = request.json["link"]
        begin = request.json["begin"]
        end = request.json["end"]
        roomsId = request.json["roomsId"]

        token = request.headers.get('Authorization')
        if token is None:
            ownerId = "undefined"
        else:
            if token[:7] != 'Bearer ':
                abort(401, description='Invalid token.')
            else:
                token = token[7:]
            ownerId = get_id_from_token(token)
            if type(ownerId) == str:
                abort(401, description=ownerId)

        try:
            user = db.session.execute(db.select(User).filter_by(id=ownerId)).scalar_one()
        except NoResultFound:
            abort(401, description='User with provided token doesnt exist.')
        else:
            password = generate_password()

            new_event = Event(name=name, description=description, link=link, editPassword=hash_password(password),
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

            user.events.append(new_event)

            db.session.commit()

            return jsonify({"id": new_event.id, "password": password})

    @app.route("/event/<event_id>", methods=["PATCH"])
    def patch_event(event_id):
        """
        Update an event with the given event_id.

        Args:
            event_id (str): The ID of the event to be updated.

        Returns:
            dict: A JSON response containing the updated event ID and password.

        Raises:
            400: If the number of query parameters is invalid.
            400: If the eventId parameter is invalid.
            400: If the password is invalid.
            400: If the begin date is greater than the end date.
            400: If the event duration is shorter than 15 minutes.
            400: If the begin and end date are not the same.
            400: If the begin date is invalid.
        """
        if len(request.args) != 1:
            abort(400, "Invalid number of query parameters")
        password = request.args.get("password", type=str)
        try:
            event = db.session.execute(db.select(Event).filter_by(id=event_id)).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid value for eventId parameter.')
        else:
            if password is None or hash_password(password) != event.editPassword:
                abort(400, "Invalid password")

            event.name = request.json["name"]
            event.description = request.json["description"]
            event.link = request.json["link"]
            begin = datetime.strptime(request.json["begin"], DATE_FORMAT)
            end = datetime.strptime(request.json["end"], DATE_FORMAT)

            event_duration = end - begin
            if begin >= end:
                abort(400, description='Begin date is greater than end date.')
            if event_duration < timedelta(minutes=15):
                abort(400, description='Event duration cant be shorter than 15 minutes.')
            if begin.date() != end.date():
                abort(400, description='Begin and end date have to be the same.')
            if begin <= datetime.today():
                abort(400, description='Invalid begin date.')

            event.begin = begin
            event.end = end

            db.session.commit()

            return jsonify({"id": event.id, "password": password})

    @app.route("/event/<event_id>/user", methods=["POST"])
    def add_participant_to_event(event_id):
        """
        Add a participant to an event.

        Args:
            event_id (str): The ID of the event.

        Returns:
            str: A JSON response indicating that the participant has been added.

        Raises:
            401: If the token is invalid.
            400: If the event ID is invalid, the user is not the owner of the event,
                 the email is not provided, or the user with the provided email already exists.

        """
        token = request.headers.get('Authorization')
        if token is None or token[:7] != 'Bearer ':
            abort(401, description='Invalid token.')
        else:
            token = token[7:]
            ownerId = get_id_from_token(token)
            if type(ownerId) == str:
                abort(401, description=ownerId)

            try:
                event = db.session.execute(db.select(Event).filter_by(id=event_id)).scalar_one()
            except NoResultFound:
                abort(400, description='Invalid value for eventId parameter.')
            else:
                if event.ownerId != ownerId:
                    abort(400, description='Only owner can add participants.')

                email = request.json["email"]

                if email is None:
                    abort(400, description='Email must be provided')

                try:
                    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
                except NoResultFound:
                    abort(400, description='User with provided email doesnt exist.')
                else:
                    for existing_user in event.users:
                        if existing_user == user:
                            abort(400, description="User with provided email is already assigned.")
                    user.events.append(event)
                    db.session.commit()

                return jsonify("Participant had been added.")

    @app.route('/register', methods=['POST'])
    def register():
        """
        Register a new user.

        This endpoint allows users to register by providing their email, first name, last name, and password.
        The provided information is validated, and if valid, a new user is created in the database.

        Returns:
            A JSON response containing a token for the registered user.

        Raises:
            400 Bad Request: If any of the required variables are missing or invalid.
        """
        email = request.json["email"]
        firstName = request.json["firstName"]
        lastName = request.json["lastName"]
        password = request.json["password"]

        if None in (email, firstName, lastName, password):
            abort(400, description='All variables must be provided')
        if len(password) < 6:
            abort(400, description='Password cannot be shorter than 6 characters')
        if not validate_email(email):
            abort(400, description='Invalid email.')

        try:
            db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        except NoResultFound:
            pass
        else:
            abort(400, description='User with provided email already exist.')

        user = User(email=email, firstName=firstName, lastName=lastName, password=hash_password(password), role_id=1)

        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id)
        return jsonify({"token": token})

    @app.route('/login', methods=['POST'])
    def login():
        """
        Logs in a user by verifying their email and password.

        Returns:
            A JSON response containing a token if the login is successful.

        Raises:
            400: If the email and password combination is invalid.
        """
        email = request.json["email"]
        password = request.json["password"]

        try:
            user = db.session.execute(db.select(User).filter_by(email=email, password=hash_password(password))).scalar_one()
        except NoResultFound:
            abort(400, description='Invalid email and password.')
        else:
            token = generate_token(user.id)
            return jsonify({"token": token})

    def get_logged_user():
        """
        Retrieves the logged-in user based on the provided token in the request headers.

        Returns:
            The logged-in user object.

        Raises:
            401: If the token is invalid or the user does not exist.
        """
        token = request.headers.get('Authorization')
        if token is None or token[:7] != 'Bearer ':
            abort(401, description='Invalid token.')
        else:
            token = token[7:]

        userId = get_id_from_token(token)
        try:
            user = db.session.execute(db.select(User).filter_by(id=userId)).scalar_one()
        except NoResultFound:
            abort(401, description='Invalid token.')
        else:
            return user

    @app.route('/user', methods=['GET'])
    def get_logged_user_data():
        """
        Retrieves the data of the logged-in user.

        Returns:
            A JSON response containing the user's data.
        """
        user = get_logged_user()
        return jsonify(user.obj_to_dict())

    @app.route('/user/events', methods=['GET'])
    def get_events_for_user():
        """
        Retrieves events for a specific user.

        Returns:
            A JSON response containing a list of events for the user, sorted by the 'begin' attribute.
        """
        token = request.headers.get('Authorization')
        if token is None or token[:7] != 'Bearer ':
            abort(401, description='Invalid token.')
        else:
            token = token[7:]

        limit = request.args.get("limit", default=20, type=int)
        if 0 > limit or limit > 20:
            abort(400, description='Invalid value for limit parameter.')

        userId = get_id_from_token(token)

        events = db.session.execute(db.select(Event).filter_by(ownerId=userId)).all()
        result = [event[0].obj_to_dict() for event in events]
        sorted_result = sorted(result, key=lambda x: x['begin'])

        return jsonify(sorted_result[:limit])

    @app.route('/user/<user_id>', methods=['PATCH'])
    def change_user_role(user_id):
        """
        Change the role of a user.

        Args:
            user_id (int): The ID of the user to change the role for.

        Returns:
            str: A JSON response indicating that the role has been changed.

        Raises:
            401: If the logged-in user is not an administrator or if the user ID is invalid.
            400: If the provided role ID is invalid.

        """
        logged_user = get_logged_user()
        if logged_user.role_id != 4:
            abort(401, description="Only administrator can change user role.")
        else:
            try:
                user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
            except NoResultFound:
                abort(401, description='Invalid userId.')
            else:
                roleId = int(request.json["roleId"])
                if roleId not in (1, 2, 3, 4):
                    abort(400, "Invalid roleId value")
                user.role_id = roleId

                db.session.commit()

                return jsonify("Role has been changed!")

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        admin = db.session.execute(db.select(User).filter_by(email="admin")).scalar_one()
        if admin is None:
            admin = User(email="admin", password="admin", role_id=4)
            db.session.add(admin)
            db.session.commit()

    app.run()
