from data.db_session import create_session


def get_object_by_id(object_id, Object):
    """Достает из БД Object с id=object_id
    :param object_id: id объекта
    :param Object: класс объекта
    :return:
    """
    return create_session().query(Object).filter(Object.id == object_id).first()


def parse_object_ids(object_ids: str, Object, separate=";") -> list:
    """
    :param object_ids: id объектов, которые нужно преобразовать в Object
    :param Object: класс объектов
    :param separate: разделитель объектов в строке
    """
    if len(object_ids) == 0:
        return []

    objects = []
    for object_id in object_ids.split(separate):
        my_object = get_object_by_id(object_id, Object)
        objects.append(my_object)

    return objects
