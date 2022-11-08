from __future__ import annotations
import json
from json import JSONDecodeError


class Message(dict):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: str) -> Message:
        message = Message(json.loads(data))
        if 'type' not in message:
            raise ValueError("Message doesn't contain 'type' field")
        return message

    @property
    def type(self) -> str:
        return self['type']

    def __str__(self):
        return json.dumps(self)
