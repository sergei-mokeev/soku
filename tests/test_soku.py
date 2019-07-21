from unittest import TestCase
from datetime import datetime
from dataclasses import dataclass
from soku import Class, Attribute


def is_int(_, value):
    return type(value) is int


def timestamp_to_date(value):
    return datetime.fromtimestamp(value)


def date_to_timestamp(value):
    return int(value.timestamp())


@dataclass
class FullName(Class):
    first_name: str = Attribute(key='firstName')
    last_name: str = Attribute(key='lastName')


@dataclass
class Person(Class):
    id: int = Attribute(validate=is_int)
    full_name: FullName = Attribute(key='fullName', attach=FullName)


@dataclass
class User(Person):
    birthday: datetime = Attribute(deserialize=timestamp_to_date, serialize=date_to_timestamp)


class Tests(TestCase):
    def test_create_instance_and_serialize(self):
        full_name = FullName('John', 'Smith')
        date = datetime.fromtimestamp(1193875200)
        user = User(12345, full_name, date)
        self.assertEqual(user.id, 12345)
        self.assertIsInstance(user.full_name, FullName)
        self.assertIsInstance(user.birthday, datetime)
        self.assertEqual(user.full_name.first_name, 'John')
        self.assertEqual(
            user.serialize(),
            {'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}}
        )

    def test_deserialize_and_serialize(self):
        user = User.deserialize(
            {'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}})
        self.assertEqual(user.id, 12345)
        self.assertIsInstance(user.full_name, FullName)
        self.assertIsInstance(user.birthday, datetime)
        self.assertEqual(user.full_name.first_name, 'John')
        self.assertEqual(
            user.serialize(),
            {'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}}
        )

    def test_validate(self):
        with self.assertRaises(ValueError) as context:
            User.deserialize(
                {'id': '12345', 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}})
        self.assertIn('Key id validation error.', context.exception.args)
