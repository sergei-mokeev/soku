SoKu - serialize and deserialize python object to JSON and back.
====

# About

Small library for serialize and deserialize python object to JSON and back. This library is useful for conversation between microservices, see examples. It can to serialize from object and back, validate when deserialize and use custom serializer.

# Installation

```bash
pip install soku
```

# Create class

```python
import soku


class Message(soku.Class):
    version = soku.Attribute()
    service = soku.Attribute()
    data = soku.Attribute()
    
``` 

# Deserialize from dictionary to message object and back

```python
import soku


dct = {'version': '1.0', 'service': 'gateway', 'data': [1, 2, 3, 4, 5]}


# try find class by dictionary attributes
message = soku.Class.deserialize(dct)

# or choice class for deserialization
message = Message.deserialize(message.serialize())

print(message.serialize())  # {'version': '1.0', 'service': 'gateway', 'data': [1, 2, 3, 4, 5]}
print(message.version)   # 1.0

for item in message.data:
    print(item)  # 1 2 3 4 5

```

# Validation and custom serialize/deserialize

```python
import soku
from datetime import datetime


class OneOf:
    def __init__(self, lst):
        self.lst = lst
        
    def __call__(self, name, value):
        if value not in self.lst:
            raise ValueError(f'Attribute {name} validation error')
        return True
        
        
def pre(value):
    return datetime.fromtimestamp(value)


def post(value):
    return int(value.timestamp())


class Message(soku.Class):
    version = soku.Attribute(validate=OneOf(['1.0', '2.0']))
    date = soku.Attribute(serialize=pre, deserialize=post)


obj = soku.Class.deserialize({'date': 1562487966, 'version': '1.0'})

print(obj.date)  # 2019-07-07 11:26:06

```