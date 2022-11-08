from __future__ import annotations

from typing import TYPE_CHECKING

from websockets.legacy.server import WebSocketServerProtocol

from quizquest.client import Client
from quizquest.message import Message

if TYPE_CHECKING:
    from quizquest.game import Game


class Manager(Client):
    def __init__(self, ws: WebSocketServerProtocol, game: Game) -> None:
        super().__init__(ws)
        self.game = game

    async def handle_incoming_message(self, message: Message) -> None:
        print(f"manager handling message: '{message}'")
