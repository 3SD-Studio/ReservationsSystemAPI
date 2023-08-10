import pytest
from project import create_app
from project.models import *


@pytest.fixture()
def app():
    app = create_app("sqlite:///db.db")

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


