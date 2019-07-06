from inspect import getmembers


class Meta(type):
    __soku_clss__ = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls.__soku_attrs__ = {k: v for k, v in getmembers(cls) if isinstance(v, Attribute)}
        key = sum([hash(a) for a in sorted(cls.__soku_attrs__)])
        mcs.__soku_clss__[key] = cls
        return cls


class Attribute:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Class(metaclass=Meta):
    def serialize(self) -> dict:
        return {k: self.__dict__.get(k) for k in self.__soku_attrs__}

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
