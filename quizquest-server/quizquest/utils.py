from asyncio import TaskGroup, get_event_loop
from functools import wraps
from random import sample
from typing import NoReturn, Awaitable, ParamSpec, TypeVar, Callable, Coroutine, Sequence


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


P = ParamSpec('P')
T = TypeVar('T')


def asyncify(func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        loop = get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return wrapper


def shuffled(seq: Sequence[T]) -> list[T]:
    return sample(seq, k=len(seq))
