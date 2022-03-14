from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from service.user_service import get_all_students
from service.group_service import save_group

teacher_page = Blueprint("teacher_page", __name__, template_folder="templates")


@teacher_page.route("/teachers/profile", methods=["GET", "POST"])
@login_required
def student_profile():
    # TODO: role only TEACHER

    name = current_user.name + " " + current_user.patronymic
    if request.method == "POST":
        if request.form.get("button") == "Создать курс":
            return redirect("/teachers/create-group")
    return render_template("teacher_profile.html", title="Профиль", name=name)


@teacher_page.route("/teachers/create-group", methods=["GET"])
@login_required
def create_group_get():
    # TODO: role only TEACHER
    students = get_all_students()
    return render_template("create_group.html", students=students)


@teacher_page.route("/teachers/create-group", methods=["POST"])
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

    return redirect("/teachers/profile")
