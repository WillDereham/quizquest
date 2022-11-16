from asyncio import TaskGroup
from typing import NoReturn, Coroutine, Awaitable


class TaskEnded(Exception):
    pass


async def _throw_on_exit(coro: Awaitable) -> NoReturn:
    await coro
    raise TaskEnded()


async def wait_first(*coros) -> None:
    try:
        async with TaskGroup() as tg:
            for coro in coros:
                tg.create_task(_throw_on_exit(coro))
    except* TaskEnded:
        pass
