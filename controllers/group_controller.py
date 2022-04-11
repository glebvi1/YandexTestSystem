import logging

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from controllers import MARK_COLORS
from data.group import Group, Module
from service.general_service import get_object_by_id
from service.group_service import get_all_modules_by_group_id, save_module, upload_materials
from service.test_service import get_all_tests_by_module_id, get_marks_by_tests
from service.user_service import is_teacher, is_student

group_page = Blueprint("group_page", __name__, template_folder="templates")


@group_page.route("/teacher/group/<int:group_id>", methods=["GET", "POST"])
@group_page.route("/student/group/<int:group_id>", methods=["GET"])
@login_required
def group_i(group_id):
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
                           group_name=group_name, group_id=group_id, message=message, module_id=None)


@group_page.route("/teacher/group/<int:group_id>/module/<int:module_id>", methods=["GET"])
@group_page.route("/student/group/<int:group_id>/module/<int:module_id>", methods=["GET"])
@login_required
def module_i_get(group_id, module_id):
    role = request.path.split("/")[1]
    marks = []
    module_name = get_object_by_id(module_id, Module).name

    tests = get_all_tests_by_module_id(module_id)

    if role == "student" and is_student(current_user):
        marks = get_marks_by_tests(tests, current_user.id)

    return render_template("module.html", group_id=group_id, module_id=module_id,
                           tests=tests, role=role, marks=marks, colors=MARK_COLORS,
                           module_name=module_name)


@group_page.route("/teacher/group/<int:group_id>/module/<int:module_id>", methods=["POST"])
@login_required
def module_i_post(group_id, module_id):
    if not is_teacher(current_user):
        return abort(403)
    if request.form.get("button") == "Создать тест":
        return redirect(f"/teacher/group/{group_id}/module/{module_id}/create-test")
    if request.form.get("button2") == "Прикрепить материалы":
        materials = request.files.getlist("files")
        upload_materials(group_id, module_id, materials)
        return redirect(f"/teacher/group/{group_id}/module/{module_id}")
