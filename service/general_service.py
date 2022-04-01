from typing import List, Tuple

from data.db_session import create_session


def parse_object_ids(object_ids: str, Object) -> list:
    if len(object_ids) == 0:
        return []
    session = create_session()
    objects = []
    for object_id in object_ids.split(";"):
        my_object = session.query(Object).filter(Object.id == object_id).first()
        objects.append(my_object)

    return objects


def get_object_by_id(object_id, Object):
    return create_session().query(Object).filter(Object.id == object_id).first()


def get_statistics(data: List[str]):
    int_data = tuple(filter(lambda a: a is not None, data))
    int_data = tuple(map(int, int_data))

    return __min(int_data), __mean(int_data), __max(int_data)


def __mean(data: Tuple[int]):
    return round(sum(data) / len(data), 2) if len(data) != 0 else 0


def __min(data: Tuple[int]):
    return min(data) if len(data) != 0 else 0


def __max(data: Tuple[int]):
    return max(data) if len(data) != 0 else 0
