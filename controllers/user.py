import re
from flask import Blueprint, redirect, render_template, request, session, url_for
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
    teste = execute("SELECT email FROM users")
    print(teste)
    query_response = execute(
        "SELECT email, username FROM users WHERE email = ? OR username = ?",
        (
            email,
            username,
        ),
    )
    print(query_response)
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
        "INSERT INTO users (username, email, hash) VALUES (?,?,?)",
        (username, email, generate_password_hash(password)),
    )
    return redirect(url_for("user.login"))
