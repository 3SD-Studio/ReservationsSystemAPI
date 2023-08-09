import hashlib
import re


def hash_password(password):
    hashedPassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashedPassword


def validate_email(email):
    return re.search(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email)
