from inspect import getmembers


class Error(Exception):
    pass


class Meta(type):
    __classes__ = {}

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        attrs = {attr: obj.kind for attr, obj in getmembers(cls) if isinstance(obj, Attribute)}
        if attrs:
            Meta.__classes__.update({cls: attrs})
        return cls


class Attribute:
    def __init__(self, kind, *, validate=None):
        self.kind = kind
        self.validate = validate

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if self.validate and not self.validate(value):
            raise Error(f'Validation error for attribute {self.name}.')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Class(metaclass=Meta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(dct):
        for cls, attrs in Class.__classes__.items():
            if attrs == {attr: type(value) for attr, value in dct.items()}:
                return cls(**dct)
        raise Error('Class with this attributes not found.')
