from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    login = EmailField("Логин", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])

    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])

    login = EmailField("Логин", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired()])

    recaptcha = RecaptchaField()
    submit = SubmitField("Зарегистрироваться")
