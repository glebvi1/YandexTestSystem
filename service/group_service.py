import logging

from data.db_session import create_session
from data.group import Group, Module
from data.user import User
from service.general_service import parse_object_ids, get_object_by_id


def save_group(name, students, teacher):
    session = create_session()

    students_id = [str(student.id) for student in students]
    group = Group(name, ";".join(students_id), teacher.id)
    session.add(group)
    session.commit()
    group_id = group.id
    connect_group_id_with_users_ids(group_id, students, teacher)

    logging.info("Group created")


def connect_group_id_with_users_ids(group_id, students, teacher):
    session = create_session()
    for student in students:
        user = session.query(User).filter_by(id=student.id).first()
        user.append_group_id(group_id)

    user = session.query(User).filter_by(id=teacher.id).first()
    user.append_group_id(group_id)

    session.commit()


def get_all_group_by_user(user: User):
    session = create_session()
    list_groups = []

    if len(user.groups_id) == 0:
        return []

    for group_id in user.groups_id.split(";"):
        group = session.query(Group).filter(Group.id == group_id).first()
        list_groups.append(group)

    return list_groups


def get_all_modules_by_group_id(group_id):
    modules_id = get_object_by_id(group_id, Group).modules_id

    modules = parse_object_ids(modules_id, Module)
    return modules if len(modules) != 0 else []


def save_module(group_id, name) -> bool:
    session = create_session()

    module_from_db = session.query(Module).filter(Module.name == name)
    if module_from_db is not None:
        return False

    module = Module(name, group_id)
    session.add(module)
    session.commit()
    session.refresh(module)
    session.expunge(module)
    session.close()

    session = create_session()
    group = session.query(Group).filter(Group.id == group_id).first()
    group.append_module_id(module.id)
    session.commit()

    return True
