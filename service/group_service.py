from data.db_session import create_session
from data.group import Group
from data.user import User


def save_group(name, students, teacher):
    session = create_session()

    students_id = [str(student.id) for student in students]
    group = Group(name, ";".join(students_id), teacher.id)
    session.add(group)
    session.commit()
    group_id = group.id
    connect_group_id_with_users_ids(group_id, students, teacher)
    

def connect_group_id_with_users_ids(group_id, students, teacher):
    session = create_session()
    for student in students:
        user = session.query(User).filter_by(id=student.id).first()
        user.append_group_id(group_id)

    user = session.query(User).filter_by(id=teacher.id).first()
    user.append_group_id(group_id)

    session.commit()


def get_all_group_by_teacher(teacher: User):
    session = create_session()
    list_groups = []

    if len(teacher.groups_id) == 0:
        return []

    for group_id in teacher.groups_id.split(";"):
        group = session.query(Group).filter(Group.id == group_id).first()
        list_groups.append(group)

    return list_groups
