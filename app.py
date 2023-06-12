from flask import Flask, redirect, session, url_for
from os import environ
from controllers.user import user_blueprint

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")


app.register_blueprint(user_blueprint, url_prefix="/user")


@app.route("/")
def index():
    if "username" in session:
        return f'Logged as {session["username"]}!'
    return redirect(url_for("user.login"))
