from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    groups_id = Column(Integer, ForeignKey("groups.groups_id"))
    group = relationship("Users")

