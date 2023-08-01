from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa


db = SQLAlchemy()


class Role(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)


class Room(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    projector = sa.Column(sa.Boolean)
    airconditioning = sa.Column(sa.Boolean)
    tv = sa.Column(sa.Boolean)
    ethernet = sa.Column(sa.Boolean)
    wifi = sa.Column(sa.Boolean)
    whiteboard = sa.Column(sa.Boolean)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    firstName = sa.Column(sa.String)
    lastName = sa.Column(sa.String)
    password = sa.Column(sa.String) #hashed JIC
    role_id = sa.Column(sa.Integer, sa.ForeignKey(Role.id))


class Event(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    link = sa.Column(sa.String)
    begin = sa.Column(sa.DateTime, nullable=False)
    end = sa.Column(sa.DateTime, nullable=False)
    ownerId = sa.Column(sa.ForeignKey(User.id))


room_event_m2m = db.Table(
    "room_event",
    sa.Column("room_id", sa.ForeignKey(Room.id), primary_key=True),
    sa.Column("event_id", sa.ForeignKey(Event.id), primary_key=True),
)


user_event_m2m = db.Table(
    "user_event",
    sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    sa.Column("event_id", sa.ForeignKey(Event.id), primary_key=True),
)
