from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from data.group import Group, Module
from service.general_service import get_statistics, get_object_by_id
from service.group_service import get_all_group_by_user
from service.test_service import get_marks_by_tests, get_all_tests_by_group_id, get_all_tests_by_module_id
from service.user_service import is_student

student_page = Blueprint("student_page", __name__, template_folder="templates")


@student_page.route("/student/profile", methods=["GET"])
@login_required
def student_profile():
    if not is_student(current_user):
        return abort(403)

    groups = get_all_group_by_user(current_user)
    name = current_user.name + " " + current_user.patronymic

    return render_template("student_profile.html", name=name, groups=groups)


@student_page.route("/student/group/<int:group_id>/statistics", methods=["GET"])
@login_required
def group_statistics(group_id):

    group_name = get_object_by_id(group_id, Group).name

    all_tests = get_all_tests_by_group_id(group_id)
    marks = get_marks_by_tests(all_tests, current_user.id)
    minn, mean, maxx = get_statistics(marks)

    return render_template("statistics.html", role="student", group_id=group_id,
                           minn=minn, mean=mean, maxx=maxx, group_name=group_name,
                           named="курс", module_name=None)


@student_page.route("/student/group/<int:group_id>/module/<int:module_id>/statistics", methods=["GET"])
@login_required
def module_statistics(group_id, module_id):

    group_name = get_object_by_id(group_id, Group).name
    module_name = get_object_by_id(group_id, Module).name

    all_tests = get_all_tests_by_module_id(module_id)
    marks = get_marks_by_tests(all_tests, current_user.id)
    minn, mean, maxx = get_statistics(marks)

    return render_template("statistics.html", role="student", group_id=group_id,
                           minn=minn, mean=mean, maxx=maxx, group_name=group_name, module_name=module_name,
                           named="модуль")
