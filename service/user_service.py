import uuid
from smtplib import SMTPRecipientsRefused
from threading import Thread

from flask_mail import Message

from data.db_session import create_session
from data.user import User
from strings import TEXT_RESET_PASSWORD


def get_all_students():
    return create_session().query(User).filter((User.roles.any(name="STUDENT"))
                                               & (User.activated_code == None))


def find_user_by_login(login: str):
    return create_session().query(User).filter(User.login == login).first()


def is_teacher(user: User):
    return user.roles[0].name == "TEACHER" and user.activated_code is None


def is_student(user: User):
    return user.roles[0].name == "STUDENT" and user.activated_code is None


def send_email(title, text, recipient_email):
    """Отправка письма на почту
    :param title: тема письма
    :param text: текст письма
    :param recipient_email: почта получателя
    """
    from main import app
    message = Message(title, recipients=[recipient_email])
    message.body = text

    thr = Thread(target=async_send_mail, args=[app, message])
    thr.start()


def async_send_mail(app, msg):
    """Отправка письма в отдельном потоке"""
    from main import mail
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPRecipientsRefused:
            pass


def activate_account(code: str) -> bool:
    """Активация аккаунта
    :param code: код активации
    """
    session = create_session()
    user_from_db: User = session.query(User).filter(User.activated_code == code).first()

    if user_from_db is None:
        return False

    user_from_db.activated_code = None
    session.commit()

    return True


def verify_email(email: str) -> bool:
    """Проверяем почту на нахождение в БД
    :param email: почта, которую нужно проверить
    True - если пользователь, с такой почтой существует
    """
    user_from_db = find_user_by_login(email)
    return user_from_db is not None


def forgot_password(email):
    session = create_session()
    user = session.query(User).filter(User.login == email).first()

    code = str(uuid.uuid4())
    user.forgot_password_code = code
    session.commit()

    text = TEXT_RESET_PASSWORD.format(code)
    send_email("Восстановление пароля", text, email)


def check_forgot_password_code(code) -> bool:
    return create_session().query(User).filter(User.forgot_password_code == code).first() is not None


def reset_password(code, new_password):
    session = create_session()
    user = session.query(User).filter(User.forgot_password_code == code).first()
    if user is None:
        return
    user.set_password(new_password)
    user.forgot_password_code = None
    session.commit()
