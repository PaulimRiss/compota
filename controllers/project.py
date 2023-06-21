from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from utils.login import login_required
from utils.querydb import execute
from utils.date import get_str_date

project_blueprint = Blueprint("project", __name__)


@project_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create_project.html")
    else:
        title, desc = request.form.get("title"), request.form.get("desc")
        if title and desc and len(title) > 0 and len(desc) > 0:
            now = get_str_date()
            execute(
                "INSERT INTO projects (title, description, createdAt) VALUES (?, ?, ?)",
                (title, desc, now),
            )
            user_id = session.get("user_id")
            project_id = execute("SELECT id FROM projects WHERE createdAt = ?", (now,))[
                0
            ]["id"]
            execute(
                "INSERT INTO roles (user_id, project_id, role, admin) VALUES (?, ?, ?, ?)",
                (user_id, project_id, "admin", True),
            )
            return redirect(url_for("project.list_projects"))
        else:
            abort(400)


@project_blueprint.route("/list")
def list_projects():
    projects = execute("SELECT * FROM projects")
    return render_template("list_projects.html", projects=projects)


@project_blueprint.route("/view")
def view():
    project_id = request.args.get("id")

    if not project_id:
        abort(400)
    project = execute("SELECT * FROM projects WHERE id = ?", (project_id))

    if not project:
        abort(400)
    return render_template("view_project.html", project=project[0])


@project_blueprint.route("/add_role", methods=["POST"])
@login_required
def add_role():
    project_id = request.form.get("project_id")
    role = request.form.get("role")
    username = request.form.get("username")
    admin_id = session.get("user_id")

    admin = execute(
        "SELECT admin FROM roles WHERE user_id = ? AND project_id = ?",
        (admin_id, project_id),
    )
    if not admin or not admin[0]["admin"]:
        abort(403)

    if not project_id or not role:
        abort(400)

    if username:
        user_id = execute("SELECT id FROM users WHERE username = ?", (username,))
        if not user_id:
            abort(400)
        user_id = user_id[0]["id"]
        execute(
            "INSERT INTO roles (user_id, project_id, role, admin) VALUES (?, ?, ?, ?)",
            (user_id, project_id, role, False),
        )
    else:
        execute(
            "INSERT INTO roles (project_id, role, admin) VALUES (?, ?, ?)",
            (project_id, role, False),
        )

    return redirect(url_for("project.view", id=project_id))
