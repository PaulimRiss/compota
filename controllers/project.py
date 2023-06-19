from flask import Blueprint, redirect, render_template, request, session, url_for
from utils.querydb import execute
from utils.date import get_str_date

project_blueprint = Blueprint("project", __name__)


@project_blueprint.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create_project.html")
    else:
        title, desc = request.form.get("title"), request.form.get("desc")
        if title and desc and len(title) > 0 and len(desc) > 0:
            execute(
                "INSERT INTO projects (title, description, createdAt) VALUES (?, ?, ?)",
                (title, desc, get_str_date()),
            )
            return redirect(url_for("project.list_projects"))
        else:
            return render_template("create_project.html")


@project_blueprint.route("/list")
def list_projects():
    projects = execute("SELECT * FROM projects")
    return render_template("list_projects.html", projects=projects)


@project_blueprint.route("/view")
def view():
    project_id = request.args.get("id")
    if project_id:
        project = execute("SELECT * FROM projects WHERE id = ?", (project_id))
        if project:
            return render_template("view_project.html", project=project[0])
        else:
            return redirect(url_for("project.list_projects"))
    else:
        return redirect(url_for("project.list_projects"))
