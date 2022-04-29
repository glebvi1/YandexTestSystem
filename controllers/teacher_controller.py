from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from controllers import MARK_COLORS
from data.group import Group
from service.general_service import parse_object_ids
from service.group_service import save_group, get_all_student_by_group_id, group_contains_user
from service.test_service import get_student_to_mark_in_tests, get_all_tests_by_group_id, get_all_tests_by_module_id
from service.user_service import get_all_students, is_teacher

teacher_page = Blueprint("teacher_page", __name__, template_folder="templates")


@teacher_page.route("/teacher/profile", methods=["GET"])
@login_required
def teacher_profile():
    if not is_teacher(current_user):
        return abort(403)

    name = current_user.name + " " + current_user.patronymic
    groups = parse_object_ids(current_user.groups_id, Group)

    return render_template("teacher_profile.html", title="Профиль", name=name, groups=groups, group_id=None)


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
    return render_template("create_group.html", students=students, group_id=None)


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
    teachers_group = parse_object_ids(current_user.groups_id, Group)
    for group in teachers_group:
        if group.name == name:
            return render_template("create_group.html", students=students,
                                   message="Группа с таким именем уже существует.", group_id=None)

    save_group(name, chosen_students, current_user)

    return redirect("/teacher/profile")


@teacher_page.route("/teacher/group/<int:group_id>/journal", methods=["GET"])
@login_required
def group_journal(group_id):
    if not is_teacher(current_user) or not group_contains_user(group_id, current_user.id):
        return abort(403)

    students = get_all_student_by_group_id(group_id)
    tests = get_all_tests_by_group_id(group_id)
    lst_student_to_mark = get_student_to_mark_in_tests(tests)

    return render_template("journal.html", students=students, lst_student_to_mark=lst_student_to_mark,
                           colors=MARK_COLORS, group_id=group_id, module_id=None)


@teacher_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/journal", methods=["GET"])
@login_required
def module_journal(group_id, module_id):
    if not is_teacher(current_user) or not group_contains_user(group_id, current_user.id):
        return abort(403)

    students = get_all_student_by_group_id(group_id)
    tests = get_all_tests_by_module_id(module_id)
    lst_student_to_mark = get_student_to_mark_in_tests(tests)

    return render_template("journal.html", students=students, lst_student_to_mark=lst_student_to_mark,
                           colors=MARK_COLORS, group_id=group_id, module_id=module_id)
