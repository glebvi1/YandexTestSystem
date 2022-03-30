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
