from data.db_session import create_session
from data.group import Group, Module
from data.user import User
import logging


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


def get_all_modules_by_group(group_id):
    modules_id = get_group(group_id).modules_id
    print(modules_id)
    modules = parse_modules_id(modules_id)
    return modules if len(modules) != 0 else []


def parse_modules_id(modules_id):
    if len(modules_id) == 0:
        return []
    session = create_session()
    modules = []
    for module_id in modules_id.split(";"):
        module = session.query(Module).filter(Module.id == module_id).first()
        modules.append(module)
    return modules


def get_group(group_id):
    return create_session().query(Group).filter(Group.id == group_id).first()


def save_module(group_id, name):
    session = create_session()
    module = Module(name, group_id)
    session.add(module)
    session.commit()
    session.refresh(module)
    session.expunge(module)
    session.close()

    print(module.id)
    print(module.name)
    print(module.group_id)

    session = create_session()
    group = session.query(Group).filter(Group.id == group_id).first()
    group.append_module_id(module.id)
    session.commit()
