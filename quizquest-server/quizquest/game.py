from __future__ import annotations

import secrets
from typing import TYPE_CHECKING

from quizquest.manager import Manager
from quizquest.message import Message

if TYPE_CHECKING:
    from quizquest.player import Player

games = {}


class Game:
    def __init__(self) -> None:
        self.code = secrets.randbelow(900000) + 100000
        self.manager: Manager | None = None
        self.players: dict[str, Player] = {}

    def on_player_leave(self, name: str) -> None:
        self.manager.send_message(Message({'type': 'player_left', 'name': name}))
        del self.players[name]

    def on_player_join(self, player: Player) -> None:
        self.players[player.name] = player
        self.manager.send_message(
            Message({'type': 'player_joined', 'player': {'name': player.name}})
        )

    async def kick_player(self, name: str) -> None:
        try:
            player = self.players[name]
        except KeyError:
            return

        player.send_message(Message({'type': 'player_kicked'}))
        await player.disconnect()
