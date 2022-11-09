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
        match message.type:
            case 'kick_player':
                try:
                    name: str = message['name']
                except KeyError:
                    self.send_error('invalid_name')
                    return
                await self.handle_kick_player(name)

    async def handle_kick_player(self, name: str) -> None:
        await self.game.kick_player(name)
