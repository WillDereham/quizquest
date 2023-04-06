from __future__ import annotations

import asyncio
import logging
from signal import SIGTERM

import websockets

from quizquest.connection import handle_connection
from quizquest.quiz import get_firestore

port = 8080


async def main() -> None:
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(SIGTERM, stop.set_result, None)

    db = await get_firestore()
    async with websockets.serve(lambda ws: handle_connection(ws, db), ['127.0.0.1', '::1'], port):
        print(f'Server listening on port {port}')
        await stop


if __name__ == '__main__':
    asyncio.run(main())
