import hashlib
import re
import jwt 
from datetime import datetime, timedelta

SECRET_KEY = 'some key'

def hash_password(password):
    hashedPassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashedPassword


def validate_email(email):
    return re.search(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email)


def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print(token)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY,  algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'