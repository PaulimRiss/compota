from functools import wraps
from flask import redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None or session.get("user_id") is None:
            return redirect(url_for("user.login"))
        return f(*args, **kwargs)

    return decorated_function
