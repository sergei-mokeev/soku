import soku


def test(value):
    return value.upper()


class A(soku.Class):
    a = soku.Attribute()
    b = soku.Attribute()

    def __init__(self, a, b):
        self.a = a
        self.b = b


print(A(5, 6).serialize())

a = soku.Class.deserialize({'a': 'asd', 'b': 2})
print(a.serialize())
