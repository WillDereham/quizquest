from asyncio import Queue, wait, create_task, FIRST_COMPLETED, TaskGroup, Task

from websockets.exceptions import ConnectionClosedError, ConnectionClosed
from websockets.legacy.server import WebSocketServerProtocol

from quizquest.message import Message


class Client:
    def __init__(self, ws: WebSocketServerProtocol) -> None:
        self._ws = ws
        self._outgoing_messages: Queue[Message] = Queue()

    async def process_messages(self) -> None:
        try:
            async with TaskGroup() as tg:
                outgoing_task = tg.create_task(self._process_outgoing_messages())
                tg.create_task(self._process_incoming_messages(outgoing_task))
        except* ConnectionClosed:
            pass

    async def _process_outgoing_messages(self) -> None:
        while True:
            message = await self._outgoing_messages.get()
            await _send_message(self._ws, message)
            self._outgoing_messages.task_done()

    async def _process_incoming_messages(self, outgoing_task: Task) -> None:
        try:
            async for message in self._ws:
                try:
                    message = Message.from_json(message)
                except ValueError:
                    self.send_error('invalid_syntax')
                    continue
                await self.handle_incoming_message(message)
        finally:
            outgoing_task.cancel()

    def send_message(self, message: Message) -> None:
        self._outgoing_messages.put_nowait(message)

    def send_error(self, code: str, **kwargs) -> None:
        self._outgoing_messages.put_nowait(Message({'type': 'error', 'code': code} | kwargs))

    async def handle_incoming_message(self, message: Message) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        print('Disconnecting from client')
        await self._outgoing_messages.join()
        await self._ws.close()
        print('Disconnected from client')


async def _send_message(ws: WebSocketServerProtocol, message: Message) -> None:
    await ws.send(str(message))


async def send_error(ws: WebSocketServerProtocol, code: str, **kwargs) -> None:
    print(f'Sending error: {code}')
    await _send_message(ws, Message({'type': 'error', 'code': code} | kwargs))
