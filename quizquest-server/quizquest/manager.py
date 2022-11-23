from __future__ import annotations

from uuid import UUID

from websockets.legacy.server import WebSocketServerProtocol

from quizquest.client import Client, require_game_status
from quizquest.message import Message

from quizquest.game import Game, GameStatus


class Manager(Client):
    def __init__(self, ws: WebSocketServerProtocol, game: Game) -> None:
        super().__init__(ws, game)

    async def handle_incoming_message(self, message: Message) -> None:
        print(f"manager handling message: '{message}'")
        match message.type:
            case 'kick_player':
                await self.handle_kick_player(message)
            case 'start_game':
                await self.handle_start_game()
            case 'next_question':
                await self.handle_next_question()
            case _:
                self.send_error('invalid_message')

    @require_game_status(GameStatus.waiting_for_start)
    async def handle_kick_player(self, message: Message) -> None:
        try:
            player_id = UUID(message['player_id'])
        except (KeyError, ValueError):
            return self.send_error('invalid_player_id')
        await self.game.kick_player(player_id)

    @require_game_status(GameStatus.waiting_for_start)
    async def handle_start_game(self) -> None:
        if len(self.game.players) == 0:
            return self.send_error('no_players')

        await self.game.start_game()

    @require_game_status(GameStatus.question_results)
    async def handle_next_question(self) -> None:
        await self.game.next_question()
