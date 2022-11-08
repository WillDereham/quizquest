from __future__ import annotations

from string import ascii_lowercase
from typing import TYPE_CHECKING
from unicodedata import normalize

from websockets.legacy.server import WebSocketServerProtocol

from quizquest.client import Client
from quizquest.message import Message

if TYPE_CHECKING:
    from quizquest.game import Game


def get_banned_words() -> set[str]:
    with open('banned_words.txt', 'r') as f:
        return {word.strip() for word in f.readlines()}


banned_words = get_banned_words()


class Player(Client):
    def __init__(self, ws: WebSocketServerProtocol, game: Game, name: str) -> None:
        super().__init__(ws)
        self.name = name
        self.game = game
        self.score = 0

    async def handle_incoming_message(self, message: Message) -> None:
        print(f"player '{self.name}' handling message: '{message}'")


def validate_name(name: str) -> bool:
    if len(name) > 20 or len(name) == 0:
        return False

    name = normalize('NFD', name).lower()
    name = ''.join([letter for letter in name if letter in ascii_lowercase])
    words = {word for word in banned_words if word in name}
    return not len(words)
