from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index(): 
    db.session.add(Role(name = "Administrator"))
    db.session.commit()
    return jsonify("Hello World!")


app.run()