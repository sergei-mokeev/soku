import typing as t
from inspect import getmembers


class Attribute:
    def __init__(
            self,
            *,
            key: str = None,
            validate: t.Callable = None,
            deserialize: t.Callable = None,
            serialize: t.Callable = None,
            attach: t.Type['Object'] = None
    ) -> None:
        self.key = key
        self.validate = validate
        self.deserialize = deserialize
        self.serialize = serialize
        self.attach = attach

    def __set_name__(self, owner: 'Object', name: str) -> None:
        self.name = name

    def __set__(self, instance: 'Object', value: t.Any) -> None:
        instance.__dict__[self.name] = value

    def __get__(self, instance: t.Optional['Object'], owner: 'Object') -> None:
        return instance.__dict__[self.name]


class Object:
    def serialize(self) -> t.Dict:
        result = {}
        for key, attribute in {
            key: attribute for key, attribute in getmembers(self.__class__) if isinstance(attribute, Attribute)
        }.items():
            value = getattr(self, key)

            if attribute.serialize:
                value = attribute.serialize(value)

            if attribute.attach:
                value = attribute.attach.serialize(value)

            result.update({attribute.key or key: value})

        return result

    @classmethod
    def deserialize(cls, data: t.Dict) -> 'Object':
        result = {}
        for key, attribute in {
            key: attribute for key, attribute in getmembers(cls) if isinstance(attribute, Attribute)
        }.items():
            value = data.get(attribute.key or key)

            if attribute.validate and not attribute.validate(attribute.key or key, value):
                raise ValueError(f'Key {attribute.key or key} validation error.')

            if attribute.deserialize:
                value = attribute.deserialize(value)

            if attribute.attach:
                value = attribute.attach.deserialize(value)

            result.update({key: value})

        return cls(**result)
