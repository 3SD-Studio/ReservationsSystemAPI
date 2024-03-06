from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship


db = SQLAlchemy()


room_event_m2m = db.Table(
    # Reservations (room_id, event_id)
    "room_event",
    sa.Column("room_id", sa.ForeignKey('room.id')),
    sa.Column("event_id", sa.ForeignKey('event.id')),
)


user_event_m2m = db.Table(
    # Participants (event_id, user_id)
    "user_event",
    sa.Column("user_id", sa.ForeignKey('user.id')),
    sa.Column("event_id", sa.ForeignKey('event.id')),
)


class Role(db.Model):
    """
    Represents a role in the system.

    Attributes:
        id (int): The unique identifier for the role.
        name (str): The name of the role.
    """
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)


class Room(db.Model):
    """
    Represents a room in the reservations system.

    Attributes:
        id (int): The unique identifier for the room.
        name (str): The name of the room.
        description (str): The description of the room.
        capacity (int): The maximum capacity of the room.
        projector (bool): Indicates if the room has a projector.
        conditioning (bool): Indicates if the room has air conditioning.
        tv (bool): Indicates if the room has a TV.
        ethernet (bool): Indicates if the room has Ethernet connection.
        wifi (bool): Indicates if the room has WiFi.
        whiteboard (bool): Indicates if the room has a whiteboard.
        events (list): The list of events associated with the room.

    Methods:
        obj_to_dict(): Converts the Room object to a dictionary.
        obj_to_dict_short(): Converts the Room object to a dictionary with limited attributes.
    """

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    capacity = sa.Column(sa.Integer)
    projector = sa.Column(sa.Boolean)
    conditioning = sa.Column(sa.Boolean)
    tv = sa.Column(sa.Boolean)
    ethernet = sa.Column(sa.Boolean)
    wifi = sa.Column(sa.Boolean)
    whiteboard = sa.Column(sa.Boolean)
    events = relationship("Event", secondary="room_event", backref='rooms')

    def obj_to_dict(self):
        """
        Converts the Room object to a dictionary.

        Returns:
            dict: A dictionary representation of the Room object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capacity": self.capacity,
            "projector": self.projector,
            "conditioning": self.conditioning,
            "tv": self.tv,
            "ethernet": self.ethernet,
            "wifi": self.wifi,
            "whiteboard": self.whiteboard
        }

    def obj_to_dict_short(self):
        """
        Converts the Room object to a dictionary with limited attributes.

        Returns:
            dict: A dictionary representation of the Room object with limited attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capacity": self.capacity
        }


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        firstName (str): The first name of the user.
        lastName (str): The last name of the user.
        password (str): The hashed password of the user.
        role_id (int): The role ID of the user.
        events (list): The list of events associated with the user.

    Methods:
        obj_to_dict(): Converts the User object to a dictionary.
        is_authenticated(): Checks if the user is authenticated.
        is_active(): Checks if the user is active.
        is_anonymous(): Checks if the user is anonymous.
        get_id(): Gets the ID of the user.
    """
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    firstName = sa.Column(sa.String)
    lastName = sa.Column(sa.String)
    password = sa.Column(sa.String, nullable=False)
    role_id = sa.Column(sa.ForeignKey(Role.id), default="1")
    events = relationship("Event", secondary="user_event", backref='users')

    def obj_to_dict(self):
        """
        Converts the User object to a dictionary.

        Returns:
            dict: A dictionary representation of the User object.
        """
        return {
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName
        }

    def is_authenticated(self):
        """
        Checks if the user is authenticated.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return True

    def is_active(self):
        """
        Checks if the user is active.

        Returns:
            bool: True if the user is active, False otherwise.
        """
        return True

    def is_anonymous(self):
        """
        Checks if the user is anonymous.

        Returns:
            bool: False since the user is not anonymous.
        """
        return False

    def get_id(self):
        """
        Gets the ID of the user.

        Returns:
            str: The ID of the user.
        """
        return str(self.id)


class Event(db.Model):
    """
    Represents an event in the system.

    Attributes:
        id (int): The unique identifier for the event.
        name (str): The name of the event.
        description (str): The description of the event.
        link (str): The link associated with the event.
        editPassword (str): The password for editing the event.
        begin (datetime): The start time of the event.
        end (datetime): The end time of the event.
        ownerId (int): The ID of the owner of the event.

    Methods:
        obj_to_dict(): Converts the Event object to a dictionary.
    """
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    link = sa.Column(sa.String)
    editPassword = sa.Column(sa.String)
    begin = sa.Column(sa.DateTime, nullable=False)
    end = sa.Column(sa.DateTime, nullable=False)
    ownerId = sa.Column(sa.Integer, sa.ForeignKey(User.id))

    def obj_to_dict(self):
        """
        Converts the Event object to a dictionary.

        Returns:
            dict: A dictionary representation of the Event object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "editPassword": self.editPassword,
            "begin": self.begin,
            "end": self.end,
            "ownerId": self.ownerId,
        }
