import soku
import unittest
from datetime import datetime
from dataclasses import dataclass


class IsInt:
    def __call__(self, name, value):
        if isinstance(value, int):
            return True
        return False


def is_int_with_exc(name, value):
    if type(value) is not int:
        raise ValueError(f'Test validation exception in attribute {name}')
    return True


def pre(value):
    return datetime.fromtimestamp(value)


def post(value):
    return int(value.timestamp())


class A(soku.Class):
    a = soku.Attribute(validate=IsInt())
    b = soku.Attribute()

    def __init__(self, a, b):
        self.a = a
        self.b = b


class B(A):
    a = soku.Attribute(validate=is_int_with_exc, serialize=post, deserialize=pre)
    c = soku.Attribute()

    def __init__(self, a, b, c=None):
        super().__init__(a, b)
        self.c = c


class C(soku.Class):
    asd = soku.Attribute(key='ASD')

    def __init__(self, asd='default'):
        self.asd = asd


@dataclass
class D(soku.Class):
    a: soku.Attribute = soku.Attribute(attachment=A)
    c: soku.Attribute = soku.Attribute(attachment=C)


class TestSoKuCase(unittest.TestCase):
    def test_serialize(self):
        a = A(a=1, b=2)
        self.assertEqual(a.serialize(), {'a': 1, 'b': 2})

    def test_deserialize(self):
        a = soku.Class.deserialize({'a': 1, 'b': 2})
        self.assertIsInstance(a, A)
        self.assertFalse(isinstance(a, B))
        a = soku.Class.deserialize({'c': 1562487966, 'a': 1, 'b': 2})
        self.assertIsInstance(a, B)
        a = B.deserialize({'a': 1, 'b': 2})
        self.assertTrue(a.__class__.__name__ == 'B')

    def test_attr_validation(self):
        self.assertRaises(ValueError, soku.Class.deserialize, {'a': 'str', 'c': 1, 'b': 2})
        self.assertRaises(ValueError, soku.Class.deserialize, {'a': 'str', 'b': 2})

    def test_attr_serialize(self):
        a = soku.Class.deserialize({'a': 1562487966, 'c': 1, 'b': 2})
        self.assertIsInstance(a.a, datetime)

    def test_attr_deserialize(self):
        a = soku.Class.deserialize({'a': 1562487966, 'c': 1, 'b': 2})
        self.assertIsInstance(a.a, datetime)
        self.assertEqual(a.serialize(), {'a': 1562487966, 'c': 1, 'b': 2})

    def test_class_not_found(self):
        with self.assertRaises(ValueError):
            soku.Class.deserialize({'z': 1, 'y': 2})

    def test_attribute_rename(self):
        a = C(asd=123)
        self.assertEqual(a.asd, 123)
        self.assertEqual(a.serialize(), {'ASD': 123})

        a = soku.Class.deserialize({'ASD': 'test'})
        self.assertEqual(a.asd, 'test')
        self.assertEqual(a.serialize(), {'ASD': 'test'})

    def test_nested_classes(self):
        a = A(a=1, b=2)
        c = C('asd')
        d = D(a=a, c=c)
        self.assertEqual(d.serialize(), {'a': {'a': 1, 'b': 2}, 'c': {'ASD': 'asd'}})
        dd = soku.Class.deserialize({'a': {'a': 1, 'b': 2}, 'c': {'ASD': 'asd'}})
        self.assertEqual(dd.c.asd, 'asd')
        dd.c.asd = 'test'
        self.assertEqual(dd.c.asd, 'test')
        self.assertEqual(dd.serialize(), {'a': {'a': 1, 'b': 2}, 'c': {'ASD': 'test'}})

    def test_default(self):
        c = C()
        self.assertEqual(c.serialize(), {'ASD': 'default'})
