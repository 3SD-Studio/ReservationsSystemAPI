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
    # Role (id, name)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)


class Room(db.Model):
    # Room (id, name, description, capacity, hasProjector, hasConditioning,
    # hasTV, hasEthernet, hasWhiteboard, hasWiFi)
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
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capacity": self.capacity
        }


class User(db.Model):
    # User (id, email, firstName, lastName, hashedPassword, role_id)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    firstName = sa.Column(sa.String)
    lastName = sa.Column(sa.String)
    password = sa.Column(sa.String, nullable=False)  # hashed JIC
    role_id = sa.Column(sa.ForeignKey(Role.id), default="1")
    events = relationship("Event", secondary="user_event", backref='users')

    def obj_to_dict(self):
        return {
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Event(db.Model):
    # Event (id, name, description, link, editPassword, start, end, owner_id)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    link = sa.Column(sa.String)
    editPassword = sa.Column(sa.String)
    begin = sa.Column(sa.DateTime, nullable=False)
    end = sa.Column(sa.DateTime, nullable=False)
    ownerId = sa.Column(sa.Integer, sa.ForeignKey(User.id))

    def obj_to_dict(self):
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
