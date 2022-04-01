import logging

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controllers import MARK_COLORS
from data.group import Group
from service.general_service import get_object_by_id
from service.group_service import get_all_modules_by_group_id, save_module
from service.test_service import get_all_tests_by_module_id, get_marks_by_tests
from service.user_service import is_teacher

group_page = Blueprint("group_page", __name__, template_folder="templates")


@group_page.route("/teacher/group/<int:group_id>", methods=["GET", "POST"])
@group_page.route("/student/group/<int:group_id>", methods=["GET"])
@login_required
def group_(group_id):
    logging.info(f"Group id = {group_id}")
    role = request.path.split("/")[1]

    group = get_object_by_id(group_id, Group)
    group_name = group.name
    modules = get_all_modules_by_group_id(group_id)
    message = ""

    if request.method == "POST" and is_teacher(current_user):
        name = request.form.get("title")
        if save_module(group_id, name):
            return redirect(f"/teacher/group/{group_id}")
        else:
            message = "Модуль с таким названием уже существует."

    return render_template("group.html", role=role, modules=modules,
                           group_name=group_name, group_id=group_id, message=message)


@group_page.route("/teacher/group/<int:group_id>/module/<int:module_id>", methods=["GET"])
@group_page.route("/student/group/<int:group_id>/module/<int:module_id>", methods=["GET"])
@login_required
def module(group_id, module_id):
    role = request.path.split("/")[1]
    marks = []

    if request.form.get("button") == "Создать тест":
        return redirect(f"/teacher/group/{group_id}/module/{module_id}/create-test")
    tests = get_all_tests_by_module_id(module_id)

    #print("current_user")
    #print(current_user)
    #print(is_student(current_user)) error

    if role == "student":
        marks = get_marks_by_tests(tests, current_user.id)

    return render_template("module.html", group_id=group_id, module_id=module_id,
                           tests=tests, role=role, marks=marks, colors=MARK_COLORS)

