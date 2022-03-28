import logging

from flask import Blueprint, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect

from service.group_service import get_all_modules_by_group, get_group, save_module

group_page = Blueprint("group_page", __name__, template_folder="templates")


@group_page.route("/teacher/group/<int:group_id>", methods=["GET", "POST"])
@login_required
def group_teacher_get(group_id):
    logging.info(f"Group id = {group_id}")

    group = get_group(group_id)
    group_name = group.name
    modules = get_all_modules_by_group(group_id)
    print(modules)
    if request.method == "POST":
        name = request.form.get("title")
        save_module(group_id, name)
        return redirect(f"/teacher/group/{group_id}")

    return render_template("group.html", role="teacher", modules=modules,
                           group_name=group_name, group_id=group_id)


@group_page.route("/student/group/<int:group_id>", methods=["GET"])
@login_required
def group_student(group_id):
    logging.info(f"Group id = {group_id}")

    group = get_group(group_id)
    group_name = group.name
    modules = get_all_modules_by_group(group_id)

    return render_template("group.html", role="student", modules=modules, group_name=group_name)
