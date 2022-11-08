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
                incoming_task = tg.create_task(self._process_incoming_messages())
                tg.create_task(self._process_outgoing_messages(incoming_task))
        except* ConnectionClosed:
            pass

    async def _process_outgoing_messages(self, incoming_task: Task) -> None:
        while not incoming_task.done():
            message = await self._outgoing_messages.get()
            await _send_message(self._ws, message)
            self._outgoing_messages.task_done()

    async def _process_incoming_messages(self) -> None:
        async for message in self._ws:
            try:
                message = Message.from_json(message)
            except ValueError:
                self.send_error('invalid_syntax')
                continue
            await self.handle_incoming_message(message)

    def send_message(self, message: Message) -> None:
        self._outgoing_messages.put_nowait(message)

    def send_error(self, code: str, **kwargs) -> None:
        self._outgoing_messages.put_nowait(Message({'type': 'error', 'code': code} | kwargs))

    async def handle_incoming_message(self, message: Message) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        await self._ws.close()


async def _send_message(ws: WebSocketServerProtocol, message: Message) -> None:
    await ws.send(str(message))


async def send_error(ws: WebSocketServerProtocol, code: str, **kwargs) -> None:
    await _send_message(ws, Message({'type': 'error', 'code': code} | kwargs))
