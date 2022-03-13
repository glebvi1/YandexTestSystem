from flask import render_template, Blueprint
from flask import request
from flask_login import login_user
from werkzeug.utils import redirect

from data.db_session import create_session
from data.user import User
from forms.register_form import LoginForm, RegistrationForm

registration_page = Blueprint("registration_page", __name__, template_folder="templates")


@registration_page.route("/users/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.login == form.login.data).first()

        if user and user.check_password(form.password.data):
            print("Logged in successfully.")
            login_user(user)
            return redirect("/")
        error_message = "Неправильный логин или пароль"
        if user is None:
            error_message = "Такого пользователя не существует. Проверьте логин и пароль"

        return render_template("login.html", message=error_message, form=form)
    return render_template("login.html", title="Авторизация", form=form)


@registration_page.route("/students/registration", methods=["GET", "POST"])
@registration_page.route("/teachers/registration", methods=["GET", "POST"])
def registration():
    is_student = "students" in request.path
    role = "students" if is_student else "teachers"
    role_name = "STUDENT" if is_student else "TEACHER"
    form = RegistrationForm()

    if form.validate_on_submit():
        error_message = ""
        if form.password.data != form.password2.data:
            error_message = "Пароли не совпадают"

        session = create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            error_message = "Такой пользователь уже есть"

        if error_message != "":
            return render_template("registration.html", title="Регистрация", form=form, message=error_message)

        user = User(form, role_name)
        user.save()
        return redirect("/")

    return render_template("registration.html", title="Регистрация", form=form, role=role)
