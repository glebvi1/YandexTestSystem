from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile_page = Blueprint("profile_page", __name__, template_folder="templates")


@profile_page.route("/teachers/profile")
@login_required
def student_profile():
    # TODO: role only TEACHER
    name = current_user.name + " " + current_user.surname
    return render_template("teacher_profile.html", title="Профиль", name=name)
