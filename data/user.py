from flask_login import UserMixin
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase, create_session


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    roles = relationship("Role", secondary="user_roles")
    characters = relationship("Group", backref="movie", lazy="dynamic")

    def __init__(self, form, role_name):
        super().__init__()

        self.login = form.login.data
        self.set_password(form.password.data)
        self.name = form.name.data
        self.surname = form.surname.data
        self.patronymic = form.patronymic.data
        self.role_name = role_name
        self.roles = []
        self.groups = []

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def save(self):
        session = create_session()
        role = session.query(Role).filter(Role.name == self.role_name).first()
        if role is None:
            self.roles.append(Role(name=self.role_name))
            session.add(self)
            session.commit()
        else:
            session.add(self)
            session.commit()

            user_roles = UserRoles(user_id=self.id, role_id=role.id)
            session.add(user_roles)
            session.commit()


class Role(SqlAlchemyBase):
    __tablename__ = "roles"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)


class UserRoles(SqlAlchemyBase):
    __tablename__ = "user_roles"
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"))
    role_id = Column(Integer(), ForeignKey("roles.id", ondelete="CASCADE"))
