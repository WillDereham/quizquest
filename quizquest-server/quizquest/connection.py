from typing import cast
from urllib.parse import urlparse, parse_qsl

from websockets.server import WebSocketServerProtocol

from quizquest.client import send_error
from quizquest.game import games, Game, GameStatus
from quizquest.manager import Manager
from quizquest.message import Message
from quizquest.player import Player, validate_name
from quizquest.quiz import get_quiz


async def handle_connection(ws: WebSocketServerProtocol) -> None:
    url = urlparse(ws.path)
    path = url.path
    query = cast(dict[str, str], dict(parse_qsl(url.query)))
    match path:
        case '/join':
            try:
                code = int(query['code'])
            except (KeyError, ValueError):
                print(f'invalid code: {query}')
                return await send_error(ws, 'invalid_code')
            try:
                name = query['name']
            except KeyError:
                return await send_error(ws, 'invalid_name')
            await handle_player_connection(ws, code, name)
        case '/start':
            try:
                quiz_id = query['quiz_id']
            except KeyError:
                return await send_error(ws, 'invalid_quiz_id')
            await handle_manager_connection(ws, quiz_id)
        case _:
            await send_error(ws, 'invalid_path')


async def handle_player_connection(ws: WebSocketServerProtocol, code: int, name: str) -> None:
    name = name.strip()
    if not validate_name(name):
        return await send_error(ws, 'invalid_name')

    try:
        game = games[code]
    except KeyError:
        return await send_error(ws, 'game_not_found')

    if game.status != GameStatus.waiting_for_start:
        return await send_error(ws, 'game_already_started')

    if len({player for player in game.players.values() if player.name == name}):
        return await send_error(ws, 'name_taken')

    player = Player(ws, game, name)
    game.on_player_join(player)
    try:
        print(f"{code}: Player '{name}' connected")
        player.send_message(Message({'type': 'connected'}))
        await player.process_messages()
    finally:
        print(f"{code}: Player '{name}' disconnected")
        game.on_player_leave(player.id)


async def handle_manager_connection(ws: WebSocketServerProtocol, quiz_id: str) -> None:
    quiz = await get_quiz(quiz_id)

    game = Game(quiz)
    code = game.code
    games[code] = game
    manager = Manager(ws, game)
    game.manager = manager

    print(f"Game created with code {code}")
    try:
        manager.send_message(Message({'type': 'game_created', 'code': code}))
        await manager.process_messages()
    finally:
        print(f"Game with code {code} ended")
        for player in game.players.values():
            await player.disconnect()
        del games[code]


