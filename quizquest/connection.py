from asyncio import wait, FIRST_COMPLETED, create_task
from typing import cast
from urllib.parse import urlparse, parse_qsl

from websockets.exceptions import ConnectionClosedError
from websockets.server import WebSocketServerProtocol

from quizquest.client import send_error
from quizquest.game import games, Game
from quizquest.manager import Manager
from quizquest.message import Message
from quizquest.player import Player, validate_name


async def handle_connection(ws: WebSocketServerProtocol) -> None:
    url = urlparse(ws.path)
    path = url.path
    query = cast(dict[str, str], dict(parse_qsl(url.query)))
    match path:
        case '/join':
            try:
                code = int(query['code'])
            except (KeyError, ValueError):
                await send_error(ws, 'invalid_code')
                return
            try:
                name = query['name']
            except KeyError:
                await send_error(ws, 'invalid_name')
                return
            await handle_player_connection(ws, code, name)
        case '/start':
            await handle_manager_connection(ws)
        case _:
            await send_error(ws, 'invalid_path')


async def handle_player_connection(ws: WebSocketServerProtocol, code: int, name: str) -> None:
    print(f"New connection for code: {code}, name: '{name}'")

    name = name.strip()
    if not validate_name(name):
        await send_error(ws, 'invalid_name')
        return

    try:
        game = games[code]
    except KeyError:
        await send_error(ws, 'game_not_found')
        return

    if game.players.get(name) is not None:
        await send_error(ws, 'name_taken')
        return

    player = Player(ws, game, name)
    game.on_player_join(player)
    try:
        player.send_message(Message({'type': 'connected'}))
        await player.process_messages()
    finally:
        game.on_player_leave(player)


async def handle_manager_connection(ws: WebSocketServerProtocol) -> None:
    game = Game()
    code = game.code
    games[code] = game
    manager = Manager(ws, game)
    game.manager = manager

    print(f"Game created with code {code}")
    try:
        manager.send_message(Message({'type': 'game_created', 'code': code}))
        await manager.process_messages()
    finally:
        for player in game.players.values():
            await player.disconnect()
        del games[code]


