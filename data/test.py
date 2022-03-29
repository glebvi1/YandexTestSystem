from sqlalchemy import Integer, Column, String, Boolean

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    criteria = Column(String, nullable=False)

    questions_id = Column(String, nullable=True)
    marks = Column(String, nullable=True)


class Question(SqlAlchemyBase):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_quest = Column(String, nullable=False)

    answer_options = Column(String, nullable=True)


class AnswerOption(SqlAlchemyBase):
    __tablename__ = "base_questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quest = Column(String, nullable=True)  # TODO: drop
    answer = Column(String, nullable=False)
    is_right = Column(Boolean, nullable=False)
