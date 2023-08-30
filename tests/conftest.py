import pytest
from project.app import create_app
from project.models import db, User


@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()
        admin = User(email="admin", password="admin", role_id=4)
        db.session.add(admin)
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


