from functools import wraps
from flask_login import current_user


def login_required(func):
    @wraps(func)
    def wrapper():
        if current_user is None or not current_user.is_authenticated:
            return "Not Authorized", 401
        else:
            func()

    return wrapper
