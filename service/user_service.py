from data.db_session import create_session
from data.user import User


def get_all_students():
    return create_session().query(User).filter(User.roles.any(name="STUDENT"))


def find_user_by_login(login: str):
    return create_session().query(User).filter(User.login == login).first()


def is_teacher(user: User):
    return user.roles[0] == "TEACHER"


def is_student(user: User):
    return user.roles[0] == "STUDENT"
