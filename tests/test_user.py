import pytest
from project.models import User


@pytest.mark.parametrize(
    "email,firstName,lastName,password,valid",
    [
        ("test@test.com", "test", "test", "test123", True),
        ("test@test.test", "test", "test", "test123", True),
        ("test@test.", "test", "test", "test123", False),
        ("test@test", "test", "test", "test123", False),
        ("test@.com", "test", "test", "test123", False),
        ("testtest.com", "test", "test", "test123", False),
        ("@test.com", "test", "test", "test123", False),
        ("test@@test.com", "test", "test", "test123", False),
        (None, "test", "test", "test123", False),
        ("test@test.com", "test", "test", None, False),
        ("test@test.com", None, "test", "test123", False),
        ("test@test.com", "test", None, "test123", False),
        ("test@test.com", "test", "test", "test", False),
        ("test@test.com", "test", "test", "test12", True),
    ]
)
def test_registration(email, firstName, lastName, password, valid, client, app):
    data = {
        "email": email,
        "firstName": firstName,
        "lastName": lastName,
        "password": password
    }

    response = client.post("/register", json=data)

    with app.app_context():
        if valid:
            assert User.query.count() == 1 and response.status_code == 200
        else:
            assert User.query.count() == 0 and response.status_code != 200


@pytest.mark.parametrize(
    "email,password,statuscode",
    [
        ("test@test.com", "test123", 200),
        ("test1@test.com", "test123", 400),
        ("test@test.com", "test12", 400),
    ]
)
def test_login(email, password, statuscode, client, app):
    data_reg = {
        "email": "test@test.com",
        "firstName": "test",
        "lastName": "test",
        "password": "test123"
    }

    client.post("/register", json=data_reg)
    response = client.post("/login", json={"email": email, "password": password})

    assert response.status_code == statuscode
