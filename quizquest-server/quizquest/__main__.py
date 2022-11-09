from __future__ import annotations

import asyncio
from signal import SIGTERM

import websockets

from quizquest.connection import handle_connection

port = 8080


async def main() -> None:
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(SIGTERM, stop.set_result, None)
    async with websockets.serve(handle_connection, ['127.0.0.1', '::1'], port):
        print(f'Server listening on port {port}')
        await stop


if __name__ == '__main__':
    asyncio.run(main())
