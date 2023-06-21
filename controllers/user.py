import re
from venv import logger
from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from utils.date import get_str_date
from utils.querydb import execute
from werkzeug.security import check_password_hash, generate_password_hash


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        username, password = request.form.get("username"), request.form.get("password")
        if not username or not password:
            abort(400)

        query_response = execute("SELECT * FROM users WHERE username = ?", (username,))

        if len(query_response) == 0:
            abort(400)

        if not check_password_hash(query_response[0]["hash"], password):
            abort(400)

        session["username"] = username
        session["user_id"] = query_response[0]["id"]
        return redirect(url_for("index"))


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    email = request.form.get("email")
    username = request.form.get("username")
    query_response = execute(
        "SELECT email, username FROM users WHERE email = ? OR username = ?",
        (
            email,
            username,
        ),
    )
    if len(query_response):
        logger.error("User already exists")
        abort(400)

    if not email or re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is None:
        logger.error("Invalid email")
        abort(400)

    password, pass_check = request.form.get("password"), request.form.get("pass-check")

    password_regex = re.compile(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()_+={}\[\]|\\:;"\'<>,.?/~`]).{8,}$'
    )

    if password != pass_check or not password_regex.match(password):
        logger.error("Invalid password")
        abort(400)

    execute(
        "INSERT INTO users (username, email, hash, createdAt) VALUES (?,?,?,?)",
        (username, email, generate_password_hash(password), get_str_date()),
    )
    return redirect(url_for("user.login"))
