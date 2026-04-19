from functools import wraps

from flask import jsonify
from flask_login import current_user

def login_permission(*roles, err_msg=None):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'status': 401, 'err_msg': err_msg})

            if not roles:
                return function(*args, **kwargs)

            if current_user.user_role in roles:
                return function(*args, **kwargs)
            return jsonify({'status': 403, 'err_msg': 'Không đủ quyền để truy cập'})

        return decorated_function
    return decorator