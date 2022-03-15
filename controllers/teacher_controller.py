from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from service.group_service import save_group, get_all_group_by_user
from service.user_service import get_all_students

teacher_page = Blueprint("teacher_page", __name__, template_folder="templates")


@teacher_page.route("/teacher/profile", methods=["GET"])
@login_required
def teacher_profile():
    # TODO: role only TEACHER

    name = current_user.name + " " + current_user.patronymic
    groups = get_all_group_by_user(current_user)

    return render_template("teacher_profile.html", title="Профиль", name=name, groups=groups)


@teacher_page.route("/teacher/profile", methods=["POST"])
@login_required
def teacher_profile_post():
    if request.form.get("button") == "Создать курс":
        return redirect("/teacher/create-group")


@teacher_page.route("/teacher/create-group", methods=["GET"])
@login_required
def create_group_get():
    # TODO: role only TEACHER
    students = get_all_students()
    return render_template("create_group.html", students=students)


@teacher_page.route("/teacher/create-group", methods=["POST"])
@login_required
def create_group_post():
    # TODO: role only TEACHER

    students = get_all_students()
    chosen_students = []
    name = request.form.get("title")

    for student in students:
        if request.form.get(f"check{student.id}") == "on":
            chosen_students.append(student)

    save_group(name, chosen_students, current_user)

    return redirect("/teacher/profile")
