from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from service.group_service import get_all_group_by_user
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
