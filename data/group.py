from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    students_id = Column(String, nullable=False)
    teacher_id = Column(String, nullable=False)

    def __init__(self, name, students_id, teacher_id):
        self.name = name
        self.students_id = students_id
        self.teacher_id = teacher_id
