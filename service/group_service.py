from data.group import Group
from data.db_session import create_session
from data.user import User


def save_group(name, students, teacher):
    session = create_session()

    students_id = [str(student.id) for student in students]
    group = Group(name, ";".join(students_id), teacher.id)
    session.add(group)
    session.commit()
    group_id = group.id

    session = create_session()
    for student in students:
        user = session.query(User).filter_by(id=student.id).first()
        user.append_group_id(group_id)

    user = session.query(User).filter_by(id=teacher.id).first()
    user.append_group_id(group_id)

    session.commit()
