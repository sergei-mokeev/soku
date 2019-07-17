from inspect import getmembers
from typing import Callable


class Meta(type):
    __soku_clss__ = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls.__soku_attrs__ = {v.name or k: v for k, v in getmembers(cls) if isinstance(v, Attribute)}
        mcs.__soku_clss__[sum([hash(a) for a in sorted(cls.__soku_attrs__)])] = cls
        return cls


class Attribute:
    def __init__(self, *, validate: Callable = None,
                 serialize: Callable = None, deserialize: Callable = None, name: str = None):
        self.validate = validate
        self.serialize = serialize
        self.deserialize = deserialize
        self.name = name

    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value):
        if callable(self.validate) and not self.validate(self.__name, value):
            raise ValueError(f'Attribute {self.__name} validation error.')
        if callable(self.deserialize):
            value = self.deserialize(value)
        instance.__dict__[self.__name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class Class(metaclass=Meta):
    def serialize(self) -> dict:
        dct = {}
        for k, v in {k: v for k, v in getmembers(self.__class__) if isinstance(v, Attribute)}.items():
            dct.update({v.name or k: v.serialize(getattr(self, k)) if callable(v.serialize) else getattr(self, k)})
        return dct

    @classmethod
    def deserialize(cls, data: dict):
        if cls is Class:
            cls = cls.__soku_clss__.get(sum([hash(a) for a in sorted([k for k in data])]))
            if not cls:
                raise ValueError(f'Unknown class. Class with this attributes not found.')
        dct = {}
        for k, v in {k: v for k, v in getmembers(cls) if isinstance(v, Attribute)}.items():
            dct.update({k: data.get(v.name) if v.name else data.get(k)})
        return cls(**dct)
