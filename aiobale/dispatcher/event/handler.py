from __future__ import annotations

import asyncio
import contextvars
from functools import partial
import inspect
from dataclasses import dataclass, field
from magic_filter.magic import MagicFilter as OriginalMagicFilter
from typing import Awaitable, Callable, Optional, Any, List, TypeVar, Union, Dict, Tuple
from typing_extensions import ParamSpec

from ...filters.base import Filter
from ...utils.magic_filter import MagicFilter

P = ParamSpec('P')
R = TypeVar('R')

CallbackType = Callable[P, Union[R, Awaitable[R]]]


@dataclass
class CallableObject:
    callback: CallbackType
    awaitable: bool = field(init=False)

    def __post_init__(self) -> None:
        callback = inspect.unwrap(self.callback)
        self.awaitable = inspect.isawaitable(callback) or inspect.iscoroutinefunction(
            callback
        )

    async def call(self, *args: Any, **kwargs: Any) -> Any:
        callback = inspect.unwrap(self.callback)
        sig = inspect.signature(callback)
        filtered_kwargs = {}
        has_var_keyword = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )

        if has_var_keyword:
            filtered_kwargs = dict(kwargs)
        else:
            for name, param in sig.parameters.items():
                if name in kwargs:
                    filtered_kwargs[name] = kwargs[name]
                else:
                    annotation = param.annotation
                    annotation_name = (
                        annotation
                        if isinstance(annotation, str)
                        else getattr(annotation, "__name__", None)
                    )
                    if annotation_name == "Client" and "client" in kwargs:
                        filtered_kwargs[name] = kwargs["client"]
                    elif annotation_name == "FSMContext" and "state" in kwargs:
                        filtered_kwargs[name] = kwargs["state"]
                    elif annotation_name == "CommandObject" and "command" in kwargs:
                        filtered_kwargs[name] = kwargs["command"]

        wrapped = partial(callback, *args, **filtered_kwargs)
        if self.awaitable:
            return await wrapped()

        loop = asyncio.get_event_loop()
        context = contextvars.copy_context()
        wrapped = partial(context.run, wrapped)
        return await loop.run_in_executor(None, wrapped)


@dataclass
class FilterObject(CallableObject):
    magic: Optional[MagicFilter] = None

    def __post_init__(self) -> None:
        if isinstance(self.callback, OriginalMagicFilter):
            self.magic = self.callback
            self.callback = self.callback.resolve

        super(FilterObject, self).__post_init__()

        if isinstance(self.callback, Filter):
            self.awaitable = True


@dataclass
class Handler(CallableObject):
    """
    Represents an event handler with associated filters and callback.
    """

    event_type: str
    filters: Optional[List[FilterObject]] = None

    async def check(self, *args: Any, **kwargs: Any) -> Tuple[bool, Dict[str, Any]]:
        data = dict(kwargs)
        if not self.filters:
            return True, data
        for event_filter in self.filters:
            check = await event_filter.call(*args, **data)
            if not check:
                return False, data
            if isinstance(check, dict):
                data.update(check)
        return True, data
