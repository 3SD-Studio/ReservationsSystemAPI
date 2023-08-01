from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa


db = SQLAlchemy()


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
    projector = sa.Column(sa.Boolean)
    conditioning = sa.Column(sa.Boolean)
    tv = sa.Column(sa.Boolean)
    ethernet = sa.Column(sa.Boolean)
    wifi = sa.Column(sa.Boolean)
    whiteboard = sa.Column(sa.Boolean)


class User(db.Model):
    # User (id, email, firstName, lastName, hashedPassword, role_id)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    firstName = sa.Column(sa.String)
    lastName = sa.Column(sa.String)
    password = sa.Column(sa.String)  # hashed JIC
    role_id = sa.Column(sa.Integer, sa.ForeignKey(Role.id))


class Event(db.Model):
    # Event (id, name, description, link, editPassword, start, end, owner_id)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    link = sa.Column(sa.String)
    editPassword = sa.Column(sa.String)  # hashed JIC
    begin = sa.Column(sa.DateTime, nullable=False)
    end = sa.Column(sa.DateTime, nullable=False)
    ownerId = sa.Column(sa.ForeignKey(User.id))


room_event_m2m = db.Table(
    # Reservations (room_id, event_id)
    "room_event",
    sa.Column("room_id", sa.ForeignKey(Room.id), primary_key=True),
    sa.Column("event_id", sa.ForeignKey(Event.id), primary_key=True),
)


user_event_m2m = db.Table(
    # Participants (event_id, user_id)
    "user_event",
    sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    sa.Column("event_id", sa.ForeignKey(Event.id), primary_key=True),
)
