import logging
import os
from pathlib import Path
from typing import List

from config import CONFIG_DIRECTION
from data.db_session import create_session
from data.group import Group, Module
from data.user import User
from db import DIRECTORY_NAME
from service.general_service import parse_object_ids, get_object_by_id


def save_group(name: str, students: List[User], teacher: User) -> None:
    """Сохранение группы в БД
    :param name: название группы
    :param students: список студентов группы
    :param teacher: учитель группы
    """
    session = create_session()

    students_id = [str(student.id) for student in students]
    group = Group(name, ";".join(students_id), teacher.id)
    session.add(group)
    session.commit()
    group_id = group.id
    __connect_group_id_with_users_ids(group_id, students, teacher)

    logging.info(f"Created GROUP with name = {name}")


def save_module(group_id: int, name: str) -> bool:
    """Сохранение модуля в БД
    :param group_id: id группы, в которой сохраняется млдуль
    :param name: название модуля
    """
    session = create_session()

    module_from_db = session.query(Module).filter((Module.name == name) & (Module.group_id == group_id)).first()
    if module_from_db is not None:
        logging.info(f"MODULE doesn't created with name = {name}")
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

    logging.info(f"Created MODULE with name = {name}")
    return True


def get_all_modules_by_group_id(group_id: int) -> List[Module]:
    """Достать из БД все модули по группе
    :param group_id: id группы, из которой достаем модули
    """
    group = get_object_by_id(group_id, Group)
    modules = parse_object_ids(group.modules_id, Module)
    return modules


def get_all_student_by_group_id(group_id: int) -> List[User]:
    """Достать из БД всех студентов по группе
    :param group_id: id группы, из которой достаем студентов
    """
    group = get_object_by_id(group_id, Group)
    students = parse_object_ids(group.students_id, User)
    return students


def upload_file(group_id, module_id, content, filename) -> None:
    """Загрузка материалов на сервер
    :param group_id: id группы
    :param module_id: id модуля
    """
    path = __create_dir(group_id, module_id)

    with open(os.path.join(CONFIG_DIRECTION, path, filename), "wb") as file:
        file.write(content)


def get_all_materials(group_id, module_id):
    path = DIRECTORY_NAME + f"/group{group_id}" + f"/module{module_id}/"
    return os.listdir(path)


def __create_dir(group_id, module_id):
    path = DIRECTORY_NAME + f"/group{group_id}" + f"/module{module_id}/"
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def __connect_group_id_with_users_ids(group_id: int, students: List[User], teacher: User) -> None:
    """Добавляем к пользователям id только что созданной группы
    :param group_id: id группы, которое добавляем
    :param students: список студентов, к которым добавляем id группы
    :param teacher: учитель, к которому добавляем id группы
    """
    session = create_session()
    for student in students:
        user = session.query(User).filter_by(id=student.id).first()
        user.append_group_id(group_id)

    user = session.query(User).filter_by(id=teacher.id).first()
    user.append_group_id(group_id)

    session.commit()
