from flask import render_template, Blueprint
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect

from service.user_service import find_user_by_login
from data.user import User
from forms.register_form import LoginForm, RegistrationForm

user_page = Blueprint("user_page", __name__, template_folder="templates")


@user_page.route("/users/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = find_user_by_login(form.login.data)

        if user and user.check_password(form.password.data):
            print("Logged in successfully.")
            login_user(user)
            return redirect("/teacher/profile") if "TEACHER" in current_user.roles[0].name else redirect("/")
        error_message = "Неправильный логин или пароль"
        if user is None:
            error_message = "Такого пользователя не существует. Проверьте логин и пароль"

        return render_template("login.html", message=error_message, form=form)
    return render_template("login.html", title="Авторизация", form=form)


@user_page.route("/student/registration", methods=["GET", "POST"])
@user_page.route("/teacher/registration", methods=["GET", "POST"])
def registration():
    is_student = "student" in request.path
    role = "student" if is_student else "teacher"
    role_name = "STUDENT" if is_student else "TEACHER"
    form = RegistrationForm()

    if form.validate_on_submit():
        error_message = ""
        if form.password.data != form.password2.data:
            error_message = "Пароли не совпадают"

        if find_user_by_login(form.login.data) is not None:
            error_message = "Такой пользователь уже есть"

        if error_message != "":
            return render_template("registration.html", title="Регистрация", form=form, message=error_message)

        user = User(form, role_name)
        user.save()
        return redirect("/users/login")

    return render_template("registration.html", title="Регистрация", form=form, role=role)


@user_page.route("/users/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
