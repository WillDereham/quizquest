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
        self.code = secrets.randbelow(90000) + 10000
        self.manager: Manager | None = None
        self.players: dict[str, Player] = {}

    def on_player_leave(self, player: Player):
        self.manager.send_message(Message({'type': 'player_left', 'name': player.name}))
        del self.players[player.name]

    def on_player_join(self, player: Player):
        self.players[player.name] = player
        self.manager.send_message(
            Message({'type': 'player_joined', 'player': {'name': player.name}})
        )
