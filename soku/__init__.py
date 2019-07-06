from inspect import getmembers
from typing import Callable


class Meta(type):
    __soku_clss__ = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls.__soku_attrs__ = {
            k: v for k, v in getmembers(cls) if isinstance(v, Attribute)}
        key = sum([hash(a) for a in sorted(cls.__soku_attrs__)])
        mcs.__soku_clss__[key] = cls
        return cls


class Attribute:
    def __init__(self, *, validate: Callable = None,
                 serialize: Callable = None, deserialize: Callable = None):
        self.validate = validate
        self.serialize = serialize
        self.deserialize = deserialize

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if self.validate and not self.validate(self.name, value):
            raise ValueError(f'Attribute {self.name} validation error.')
        if self.serialize:
            value = self.serialize(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        value = instance.__dict__[self.name]
        return value


class Class(metaclass=Meta):
    def serialize(self) -> dict:
        dct = {}
        for k, v in self.__soku_attrs__.items():
            dct.update({k: v.deserialize(
                self.__dict__.get(k))}) if v.deserialize else dct.update(
                {k: self.__dict__.get(k)})
        return dct

    @classmethod
    def deserialize(cls, dct: dict):
        if cls is Class:
            key = sum([hash(a) for a in sorted([k for k in dct])])
            cls = cls.__soku_clss__.get(key)
            if not cls:
                raise ValueError(f'Unknown class. Class with this attributes not found.')
            [setattr(cls, a, v) for a, v in cls.__soku_attrs__.items()]
            return cls(**dct)
        else:
            return cls(**dct)
