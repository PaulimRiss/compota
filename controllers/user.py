import re
from flask import Blueprint, redirect, render_template, request, session, url_for
from utils.date import get_str_date
from utils.querydb import execute
from werkzeug.security import check_password_hash, generate_password_hash


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")

    session["username"] = request.form.get("username")
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
        return render_template("register.html"), 400

    if not email or re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is None:
        return render_template("register.html"), 400

    password, pass_check = request.form.get("password"), request.form.get("pass-check")

    password_regex = re.compile(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()_+={}\[\]|\\:;"\'<>,.?/~`]).{8,}$'
    )

    if password != pass_check or not password_regex.match(password):
        return render_template("register.html"), 400

    execute(
        "INSERT INTO users (username, email, hash, createdAt) VALUES (?,?,?,?)",
        (username, email, generate_password_hash(password), get_str_date()),
    )
    return redirect(url_for("user.login"))
