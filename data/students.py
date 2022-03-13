from flask_login import UserMixin
from sqlalchemy import String, Integer, Column
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase

'''
class Student(SqlAlchemyBase, UserMixin):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def __init__(self, form):
        super().__init__()

        self.login = form.login.data
        self.set_password(form.password.data)
        self.name = form.name.data
        self.surname = form.surname.data

        self.groups = []

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
'''