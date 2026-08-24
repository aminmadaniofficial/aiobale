from __future__ import annotations
import sys
import asyncio
from functools import partial
import contextvars
from typing import Any, Callable, TypeVar

T = TypeVar("T")


async def to_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """
    Python 3.8+ compatible asyncio.to_thread wrapper.
    Executes a blocking callable in a separate thread.
    """
    if sys.version_info >= (3, 9):
        return await asyncio.to_thread(func, *args, **kwargs)

    loop = asyncio.get_event_loop()
    ctx = contextvars.copy_context()
    func_call = partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)
