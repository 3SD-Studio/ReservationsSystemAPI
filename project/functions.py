import hashlib
import re
import jwt
from datetime import datetime, timedelta
import secrets
import string

SECRET_KEY = 'some key'


import hashlib

def hash_password(password):
    """
    Hashes the given password using the SHA-512 algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.

    """
    hashedPassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashedPassword


def validate_email(email):
    """
    Validates if the given email address is in a valid format.

    Args:
        email (str): The email address to be validated.

    Returns:
        re.Match object or None: A re.Match object if the email is valid, None otherwise.
    """
    return re.search(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@" +
                     r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email)


def generate_token(user_id):
    """
    Generates a JWT token for the given user ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        str: The generated JWT token.
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def get_id_from_token(token):
    """
    Retrieves the user ID from the given JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        str: The user ID extracted from the token.

    Raises:
        str: If the token has expired, returns 'Signature expired. Please log in again.'
        str: If the token is invalid, returns 'Invalid token. Please log in again.'
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def get_values_from_token(token):
    """
    Retrieves the user ID from the given JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        str, datetime, datetime: user_id, expiration, issued

    Raises:
        str: If the token has expired, returns 'Signature expired. Please log in again.'
        str: If the token is invalid, returns 'Invalid token. Please log in again.'
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['sub'], payload['exp'], payload['iat']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.', datetime.now(), datetime.now()
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.', datetime.now(), datetime.now()


def generate_password():
    """
    Generates a random password consisting of letters (both uppercase and lowercase) and digits.

    Returns:
        str: The generated password.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))
