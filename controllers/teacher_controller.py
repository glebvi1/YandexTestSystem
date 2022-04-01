from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from service.group_service import save_group, get_all_group_by_user, get_all_student_by_group_id
from service.user_service import get_all_students, is_teacher

teacher_page = Blueprint("teacher_page", __name__, template_folder="templates")


@teacher_page.route("/teacher/profile", methods=["GET"])
@login_required
def teacher_profile():
    if not is_teacher(current_user):
        return abort(403)

    name = current_user.name + " " + current_user.patronymic
    groups = get_all_group_by_user(current_user)

    return render_template("teacher_profile.html", title="Профиль", name=name, groups=groups)


@teacher_page.route("/teacher/profile", methods=["POST"])
@login_required
def teacher_profile_post():
    if not is_teacher(current_user):
        return abort(403)

    if request.form.get("button") == "Создать курс":
        return redirect("/teacher/create-group")


@teacher_page.route("/teacher/create-group", methods=["GET"])
@login_required
def create_group_get():
    if not is_teacher(current_user):
        return abort(403)

    students = get_all_students()
    return render_template("create_group.html", students=students)


@teacher_page.route("/teacher/create-group", methods=["POST"])
@login_required
def create_group_post():
    if not is_teacher(current_user):
        return abort(403)

    students = get_all_students()
    chosen_students = []
    name = request.form.get("title")

    for student in students:
        if request.form.get(f"check{student.id}") == "on":
            chosen_students.append(student)

    if len(chosen_students) == 0:
        return render_template("create_group.html", students=students, message="Вы не выбрали ни одного студента.")
    teachers_group = get_all_group_by_user(current_user)
    for group in teachers_group:
        if group.name == name:
            return render_template("create_group.html", students=students,
                                   message="Группа с таким именем уже существует.")

    save_group(name, chosen_students, current_user)

    return redirect("/teacher/profile")


@teacher_page.route("/teacher/group/<int:group_id>/journal", methods=["GET"])
@login_required
def journal(group_id):

    students = get_all_student_by_group_id(group_id)
    print(students)

    return render_template("journal.html", students=students)
