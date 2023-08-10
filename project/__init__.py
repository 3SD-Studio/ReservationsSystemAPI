from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from project.models import User, db


def create_app(database_uri="sqlite:///database.db"):
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

    return app
