from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

teacher_page = Blueprint("teacher_page", __name__, template_folder="templates")


@teacher_page.route("/teachers/profile", methods=["GET", "POST"])
@login_required
def student_profile():
    # TODO: role only TEACHER
    print(current_user.roles[0].name)
    name = current_user.name + " " + current_user.patronymic
    if request.method == "POST":
        if request.form.get("button") == "Создать курс":
            return redirect("/teachers/create-group")
    return render_template("teacher_profile.html", title="Профиль", name=name)


@teacher_page.route("/teachers/create-group")
@login_required
def create_group():
    # TODO: role only TEACHER
    pass
