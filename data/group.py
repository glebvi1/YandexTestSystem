from sqlalchemy import Integer, Column, String

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    students_id = Column(String, nullable=False)
    teacher_id = Column(String, nullable=False)

    modules_id = Column(String, nullable=True)

    def __init__(self, name, students_id, teacher_id):
        self.name = name
        self.students_id = students_id
        self.teacher_id = teacher_id
        self.modules_id = ""

    def append_module_id(self, module_id):
        separate = ";"
        if len(self.modules_id) == 0:
            separate = ""
        x = self.modules_id + f"{separate}{module_id}"
        self.modules_id = x


class Module(SqlAlchemyBase):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    group_id = Column(String, nullable=False)

    tests_id = Column(String, nullable=True)

    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

        self.tests_id = ""

    def append_module_id(self, test_id):
        separate = ";"
        if len(self.tests_id) == 0:
            separate = ""
        x = self.modules_id + f"{separate}{test_id}"
        self.tests_id = x
