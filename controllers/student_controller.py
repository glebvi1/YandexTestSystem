from flask import Blueprint, render_template
from flask_login import login_required, current_user

from service.group_service import get_all_group_by_user

student_page = Blueprint("student_page", __name__, template_folder="templates")


@student_page.route("/student/profile", methods=["GET"])
@login_required
def student_profile():
    # TODO: can use only STUDENT
    groups = get_all_group_by_user(current_user)
    name = current_user.name + " " + current_user.patronymic

    return render_template("student_profile.html", name=name, groups=groups)
