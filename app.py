from flask import Flask, redirect, session, url_for
from os import environ
from controllers.user import user_blueprint
from controllers.project import project_blueprint

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")


app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(project_blueprint, url_prefix="/project")


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("project.list_projects"))
    return redirect(url_for("user.login"))
