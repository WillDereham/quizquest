from __future__ import annotations

import asyncio

import websockets

from quizquest.connection import handle_connection

port = 8080


async def main() -> None:
    async with websockets.serve(handle_connection, ['127.0.0.1', '::1'], port):
        print(f'Server listening on port {port}')
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
