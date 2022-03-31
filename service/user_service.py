from smtplib import SMTPRecipientsRefused
from threading import Thread

from flask_mail import Message

from data.db_session import create_session
from data.user import User


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
    from main import app
    message = Message(title, recipients=[recipient_email])
    message.body = text

    thr = Thread(target=async_send_mail, args=[app, message])
    thr.start()


def async_send_mail(app, msg):
    from main import mail
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPRecipientsRefused:
            pass


def activate_account(code: str):
    session = create_session()
    user_from_db: User = session.query(User).filter(User.activated_code == code).first()

    if user_from_db is None:
        return False

    user_from_db.activated_code = None
    session.commit()

    return True
