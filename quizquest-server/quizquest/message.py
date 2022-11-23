from __future__ import annotations
import json
from typing import Any
from uuid import UUID


def default(o: Any) -> Any:
    if isinstance(o, UUID):
        return str(o)
    raise TypeError()


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
        return json.dumps(self, default=default)
