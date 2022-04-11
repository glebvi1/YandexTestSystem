from sqlalchemy import Integer, Column, String, Boolean

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    criteria = Column(String, nullable=False)
    timer = Column(String, nullable=True, default=None)

    questions_id = Column(String, nullable=True)
    marks = Column(String, nullable=True)

    def append_mark(self, student_id, mark):
        separate = ";"
        inner_separate = "-"
        if self.marks is None:
            x = f"{student_id}{inner_separate}{mark}"
            self.marks = x
        else:
            x = f"{separate}{student_id}{inner_separate}{mark}"
            self.marks += x


class Question(SqlAlchemyBase):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_quest = Column(String, nullable=False)

    answer_options = Column(String, nullable=True)


class AnswerOption(SqlAlchemyBase):
    __tablename__ = "answers_options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String, nullable=False)
    is_right = Column(Boolean, nullable=False)
