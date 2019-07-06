import soku
from datetime import datetime


def valid(name, value):
    if type(value) is not int:
        raise ValueError(f'Test validation exception in attribute {name}')
    return True


def pre(value):
    return datetime.fromtimestamp(value)


def post(value):
    return int(value.timestamp())


class A(soku.Class):
    a = soku.Attribute(validate=valid, serialize=pre, deserialize=post)
    b = soku.Attribute()

    def __init__(self, a, b):
        self.a = a
        self.b = b


class B(A):
    c = soku.Attribute()

    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c


a = soku.Class.deserialize({'a': 1562423485, 'b': 2})
print(a.a)
print(a.serialize())

print(B.deserialize({'a': 1562423485, 'b': 2, 'c': 3}).serialize())
