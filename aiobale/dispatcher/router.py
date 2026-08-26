from __future__ import annotations
from collections import defaultdict
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Union,
)

from .event.handler import Handler, FilterObject, CallbackType
from .event.observer import EventObserver
from ..fsm.state import State
from ..fsm.filter import StateFilter


class Router:
    """
    Router for organizing and registering event handlers.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self.name: str = name or hex(id(self))
        self._handlers: Dict[str, List[Handler]] = defaultdict(list)
        self._observer = EventObserver()

        self._register_default_event_types()

        self.message = self._observer.get_decorator("message")
        self.message_deleted = self._observer.get_decorator("message_deleted")
        self.chat_deleted = self._observer.get_decorator("chat_deleted")
        self.chat_cleared = self._observer.get_decorator("chat_cleared")
        self.username_changed = self._observer.get_decorator("username_changed")
        self.message_sent = self._observer.get_decorator("message_sent")
        self.message_edited = self._observer.get_decorator("message_edited")
        self.about_changed = self._observer.get_decorator("about_changed")
        self.user_blocked = self._observer.get_decorator("user_blocked")
        self.user_unblocked = self._observer.get_decorator("user_unblocked")
        self.group_message_pinned = self._observer.get_decorator("group_message_pinned")
        self.group_pin_removed = self._observer.get_decorator("group_pin_removed")

    def _register_default_event_types(self) -> None:
        for event_type in (
            "message",
            "message_deleted",
            "chat_cleared",
            "chat_deleted",
            "username_changed",
            "message_sent",
            "message_edited",
            "about_changed",
            "user_blocked",
            "user_unblocked",
            "group_message_pinned",
            "group_pin_removed",
        ):
            self._observer.register(event_type, self._make_event_decorator(event_type))

    def _make_event_decorator(
        self, event_type: str
    ) -> Callable[..., Callable[..., Coroutine[Any, Any, Any]]]:
        def decorator(*filters: Any):
            return self.register(event_type, *filters)

        return decorator

    def add_event_type(self, event_type: str) -> None:
        self._observer.register(event_type, self._make_event_decorator(event_type))

    def register(
        self,
        event_type: str,
        *filters: Any,
    ) -> Callable[[CallbackType], CallbackType]:
        from ..fsm.state import StatesGroup
        normalized_filters: List[Any] = []
        for f in filters:
            if isinstance(f, (State, type)) and (isinstance(f, State) or (isinstance(f, type) and issubclass(f, StatesGroup))):
                normalized_filters.append(StateFilter(f))
            else:
                normalized_filters.append(f)

        def decorator(func: CallbackType) -> CallbackType:
            handler = Handler(
                event_type=event_type,
                callback=func,
                filters=[FilterObject(filter_) for filter_ in normalized_filters],
            )
            self._handlers[event_type].append(handler)
            return func

        return decorator

    def get_handlers(self, event_type: str) -> List[Handler]:
        return self._handlers.get(event_type, [])

    def available_event_types(self) -> List[str]:
        return list(self._handlers.keys())

    def all_handlers(self) -> Dict[str, List[Handler]]:
        return self._handlers

    def handler_count(self) -> int:
        return sum(len(handlers) for handlers in self._handlers.values())
