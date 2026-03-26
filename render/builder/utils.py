from enum import Enum

from flask import url_for
from sqlalchemy import inspect


class FieldType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIMESTAMP = "timestamp"
    IMAGE = "image"
    FILE_UPLOAD = "file_upload"
    RELATIONSHIP = "relationship"
    PASSWORD = "password"
    IMAGE_UPLOAD = "image_upload"
    RELATIONSHIP_ONE = "relationship_one"
    RELATIONSHIP_MANY = "relationship_many"
    SELECT = "select"


def outside_url_for(endpoint, **kwargs):
    def wrap_url_for(*args, **params):
        return url_for(endpoint, **{**kwargs, **params})

    return wrap_url_for


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def get_class(class_name):
    from importlib import import_module

    try:
        module_path, class_name = class_name.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_name)


def is_relationship(model_class, field):
    from sqlalchemy.orm.base import RelationshipDirection

    for rel in inspect(model_class).relationships:
        if rel.key == field:
            match rel.direction:
                case RelationshipDirection.MANYTOONE:
                    res = FieldType.RELATIONSHIP_ONE
                case RelationshipDirection.MANYTOMANY:
                    res = FieldType.RELATIONSHIP_MANY
                case RelationshipDirection.ONETOMANY:
                    res = FieldType.RELATIONSHIP_MANY
                case _:
                    res = None
            return res
    return False


def relationship_class(model_class, field):
    for rel in inspect(model_class).relationships:
        if rel.key == field:
            return rel.mapper.class_
    return None
