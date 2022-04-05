import logging

from flask import render_template, Blueprint
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data.user import User
from forms.register_form import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from service.user_service import find_user_by_login, activate_account, send_email, verify_email, forgot_password, \
    check_forgot_password_code, reset_password
from strings import TEXT_REGISTRATION

user_page = Blueprint("user_page", __name__, template_folder="templates")


@user_page.route("/users/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = find_user_by_login(form.login.data)

        if user and user.check_password(form.password.data) and user.activated_code is None:
            logging.info("Logged in successfully")
            login_user(user)
            return redirect("/teacher/profile") if "TEACHER" in current_user.roles[0].name \
                else redirect("/student/profile")

        error_message = "Неправильный логин или пароль."
        if user is None:
            error_message = "Такого пользователя не существует. Проверьте логин и пароль."
        elif user.activated_code is not None:
            error_message = "Вы не подтвердили почту."

        logging.info("Logged is badly")
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
            error_message = "Пароли не совпадают."

        if find_user_by_login(form.login.data) is not None:
            error_message = "Такой пользователь уже существует."

        if error_message != "":
            logging.info("Registration is badly")
            return render_template("registration.html", title="Регистрация", form=form, message=error_message)

        user = User(form, role_name)
        user.save()

        text = TEXT_REGISTRATION.format(user.name, user.patronymic, user.activated_code)

        send_email("Код активации", text, user.login)

        logging.info("Registration is successfully")
        return redirect("/users/login")

    return render_template("registration.html", title="Регистрация", form=form, role=role)


@user_page.route("/users/activate/<string:code>", methods=["GET", "POST"])
def activate(code: str):
    if activate_account(code):
        return redirect("/users/login")

    message = "Код активации не верен. Попробуйте еще раз."
    return render_template("activated_page.html", message=message)


@user_page.route("/users/logout")
@login_required
def logout():
    logging.info("User logout")
    logout_user()
    return redirect("/")


@user_page.route("/users/forgot_password", methods=["GET", "POST"])
def forgot_password_get_post():
    form = ForgotPasswordForm()
    message = ""

    if form.validate_on_submit():
        email = form.email.data
        if verify_email(email):
            forgot_password(email)
            return redirect("/users/login")
        else:
            message = "Такая почта не найдена!"

    return render_template("forgot_password.html", form=form, message=message)


@user_page.route("/users/reset_password/<string:code>", methods=["GET", "POST"])
def reset_password_get_post(code: str):
    if not check_forgot_password_code(code):
        return abort(404)

    form = ResetPasswordForm()
    message = ""

    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            reset_password(code, form.password.data)
            return redirect("/users/login")
        message = "Пароли не совпадают"

    return render_template("reset_password.html", form=form, code=code, message=message)
