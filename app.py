import re
from flask import Flask, redirect, request, render_template, session, url_for
from os import environ
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")


def execute(query, params=None):
    conn = sqlite3.connect(environ.get("DATABASE_PATH"))
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.commit
    conn.close
    return data


@app.route("/")
def index():
    if "username" in session:
        return f'Logged as {session["username"]}!'
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    session["username"] = request.form.get("username")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
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
    return redirect(url_for("login"))
