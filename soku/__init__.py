from typing import Callable, Type
from inspect import getmembers


class Attribute:
    def __init__(self, *, key: str = None, validate: Callable = None,
                 deserialize: Callable = None, serialize: Callable = None, attach: Type['Class'] = None):
        self.key = key
        self.validate = validate
        self.deserialize = deserialize
        self.serialize = serialize
        self.attach = attach

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Class:
    def serialize(self) -> dict:
        result = {}
        for key, attribute in {key: attribute for key, attribute
                               in getmembers(self.__class__) if isinstance(attribute, Attribute)}.items():
            value = getattr(self, key)
            if attribute.serialize:
                value = attribute.serialize(value)
            if attribute.attach:
                value = attribute.attach.serialize(value)
            result.update({attribute.key or key: value})
        return result

    @classmethod
    def deserialize(cls, data: dict) -> 'Class':
        result = {}
        for key, attribute in {key: attribute for key, attribute
                               in getmembers(cls) if isinstance(attribute, Attribute)}.items():
            value = data.get(attribute.key or key)
            if attribute.validate and not attribute.validate(attribute.key or key, value):
                raise ValueError(f'Key {attribute.key or key} validation error.')
            if attribute.deserialize:
                value = attribute.deserialize(value)
            if attribute.attach:
                value = attribute.attach.deserialize(value)
            result.update({key: value})
        return cls(**result)
