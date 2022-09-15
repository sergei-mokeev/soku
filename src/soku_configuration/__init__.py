from os import environ
from argparse import ArgumentParser


class Configuration:
    def __init__(self) -> None:
        parser = ArgumentParser()
        for key, _cls in self.__annotations__.items():
            value = None
            try:
                value = self.__getattribute__(key)

            except AttributeError:
                pass

            parser.add_argument(f'--{key}', type=_cls, default=None)
            args = parser.parse_args()

            if args.__dict__.get(key):
                value = args.__dict__[key]

            if environ.get(key):
                value = environ[key]

            if value is None:
                raise ValueError(f'Can not set configuration parameters {key}')

            if issubclass(_cls, list):
                if isinstance(value, str):
                    value = value.split(',')

                else:
                    _value = []
                    for item in value:
                        if not isinstance(item, str):
                            raise ValueError(f'List value must have only string')
                        _value.append(item)

                    value = _value

            self.__setattr__(key, _cls(value))
