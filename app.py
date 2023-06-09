from flask import Flask, redirect, request, render_template, session, url_for
from os import environ

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

@app.route("/")
def index():
    if "username" in session:
        return f'Logged as {session["username"]}!'
    return redirect(url_for("login"))

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def logged():
    session["username"] = request.form.get("username")
    return redirect(url_for("index"))
