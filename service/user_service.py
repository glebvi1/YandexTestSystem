from data.db_session import create_session
from data.user import User


def get_all_students():
    session = create_session()
    students = session.query(User).filter(User.roles.any(name="STUDENT"))

    return students


def find_user_by_login(login: str):
    session = create_session()
    return session.query(User).filter(User.login == login).first()
