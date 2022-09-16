# SoKu 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/15047237ccab49048a214be614675b1e)](https://www.codacy.com/app/SergeyMokeyev/soku?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SergeyMokeyev/soku&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/15047237ccab49048a214be614675b1e)](https://www.codacy.com/app/SergeyMokeyev/soku?utm_source=github.com&utm_medium=referral&utm_content=SergeyMokeyev/soku&utm_campaign=Badge_Coverage)

SoKu is small library for serialize and deserialize python object to JSON and back. 
This library is useful for conversation between micro services, see example. 
It can to serialize from object and back, validate when deserialize and use custom deserializer and serializer.

**Installation**

```bash
pip install soku
```

**Example**

```python
from datetime import datetime
from dataclasses import dataclass
from soku_object import Object, Attribute


def is_int(_, value):  # validator must be callable and return bool or raise exception
    return isinstance(value, int)


def timestamp_to_date(value):
    return datetime.fromtimestamp(value)


def date_to_timestamp(value):
    return int(value.timestamp())


@dataclass
class FullName(Object):
    first_name: str = Attribute(key='firstName')
    last_name: str = Attribute(key='lastName')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


@dataclass
class Person(Object):
    id: int = Attribute(validate=is_int)
    full_name: FullName = Attribute(key='fullName', attach=FullName)


@dataclass
class User(Person):
    birthday: datetime = Attribute(deserialize=timestamp_to_date, serialize=date_to_timestamp)


if __name__ == '__main__':
    # create instance and serialize
    full_name = FullName('John', 'Smith')
    user = User(12345, full_name, datetime.fromtimestamp(1193875200))
    print(user.serialize())  #  {'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}}


    # deserialize and serialize
    user = User.deserialize({'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}})
    print(user.full_name.full_name())  # John Smith
    print(user.serialize())  # {'id': 12345, 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}}

    # validate
    try:
        User.deserialize({'id': '12345', 'birthday': 1193875200, 'fullName': {'firstName': 'John', 'lastName': 'Smith'}})
    except ValueError as exc:
        print(exc)  # Key id validation error.
```
