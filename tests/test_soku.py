from soku import Class, Attribute


class B(Class):
    a = Attribute(int)
    b = Attribute(list)
    c = Attribute(dict)


class A(Class):
    a = Attribute(int)
    b = Attribute(int)


a = A(a=3, b=2)
print(a.serialize())

b = Class.deserialize({'b': [1, 2], 'c': {1: 1}, 'a': 1})
print(b.serialize())
