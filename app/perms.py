from functools import wraps

from flask import redirect, abort
from flask_login import current_user

from app.models import UserRole


def login_permission(*roles):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect("/login")

            if not roles:
                return function(*args, **kwargs)

            if current_user.user_role in roles:
                return function(*args, **kwargs)
            return abort(403)

        return decorated_function
    return decorator