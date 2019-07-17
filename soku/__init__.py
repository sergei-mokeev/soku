from inspect import getmembers, isclass
from typing import Callable


class Meta(type):
    __classes__ = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        attributes = {value.key or key: value for key, value in getmembers(cls) if isinstance(value, Attribute)}
        mcs.__classes__[sum([hash(attribute) for attribute in sorted(attributes)])] = cls
        return cls


class Attribute:
    def __init__(self, *, key: str = None, validate: Callable = None,
                 deserialize: Callable = None, serialize: Callable = None, attachment=None):
        self.key = key
        self.validate = validate if callable(validate) else None
        self.deserialize = deserialize if callable(deserialize) else None
        self.serialize = serialize if callable(serialize) else None
        self.attachment = attachment if isclass(attachment) and issubclass(attachment, Class) else None

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if self.validate and not self.validate(self.name, value):
            raise ValueError(f'Attribute {self.name} validation error.')
        if self.deserialize:
            value = self.deserialize(value)
        if self.attachment:
            value = self.attachment.deserialize(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Class(metaclass=Meta):
    def serialize(self) -> dict:
        result = {}
        for key, value in self.__dict__.items():
            attribute = self.__class__.__dict__.get(key)
            if isinstance(attribute, Attribute):
                key = attribute.key or key
                if attribute.serialize:
                    value = attribute.serialize(value)
                if attribute.attachment:
                    value = attribute.attachment.serialize(value)
            result.update({key: value})
        return result

    @classmethod
    def deserialize(cls, data: dict):
        if cls is Class:
            cls = cls.__classes__.get(sum([hash(key) for key in sorted([key for key in data])]))
            if not cls:
                raise ValueError(f'Unknown class. Class with this attributes not found.')
        result = {}
        for key, value in {k: v for k, v in getmembers(cls) if isinstance(v, Attribute)}.items():
            result.update({key: data.get(value.key) if value.key else data.get(key)})
        return cls(**result)
