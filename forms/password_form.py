from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class ForgotPasswordForm(FlaskForm):
    email = EmailField("Введите почту: ", validators=[DataRequired(), Email()])

    submit = SubmitField("Отправить письмо")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired()])

    submit = SubmitField("Сохранить новый пароль")
