from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
import inspect

from .router import Router
from ..fsm.storage.base import BaseStorage
from ..fsm.storage.memory import MemoryStorage
from ..fsm.context import FSMContext
from ..middlewares.base import BaseMiddleware


class Dispatcher(Router):
    """
    Core Dispatcher managing event routing, FSM states, and Middleware pipelines.
    
    Parameters:
        name (Optional[str]): Dispatcher name identifier.
        storage (Optional[BaseStorage]): Storage backend for FSM (defaults to MemoryStorage).
    """
    def __init__(self, name: Optional[str] = None, storage: Optional[BaseStorage] = None) -> None:
        super().__init__(name or "dispatcher")
        self.storage: BaseStorage = storage or MemoryStorage()
        self.middlewares: List[BaseMiddleware] = []

    def middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """
        Registers a middleware to the dispatcher.
        """
        self.middlewares.append(middleware)
        return middleware

    def include_router(self, router: Router) -> None:
        for event_type, handlers in router.all_handlers().items():
            self._handlers[event_type].extend(handlers)

        for event_type in router.available_event_types():
            if event_type not in self.available_event_types():
                self.add_event_type(event_type)

    def _extract_chat_and_user_ids(self, event: Any, kwargs: Dict[str, Any]) -> tuple[Optional[int], Optional[int]]:
        chat_id: Optional[int] = None
        user_id: Optional[int] = None

        if hasattr(event, "chat") and getattr(event.chat, "id", None) is not None:
            chat_id = event.chat.id
        elif "chat_id" in kwargs:
            chat_id = kwargs["chat_id"]

        if hasattr(event, "sender_id") and event.sender_id is not None:
            user_id = event.sender_id
        elif hasattr(event, "from_user") and getattr(event.from_user, "id", None) is not None:
            user_id = event.from_user.id
        elif "user_id" in kwargs:
            user_id = kwargs["user_id"]

        if chat_id is not None and user_id is None:
            user_id = chat_id
        elif user_id is not None and chat_id is None:
            chat_id = user_id

        return chat_id, user_id

    async def dispatch(self, event_type: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        event = args[0] if args else kwargs.get("event")
        
        # Extract FSM context if possible
        chat_id, user_id = self._extract_chat_and_user_ids(event, kwargs)
        state_context: Optional[FSMContext] = None
        if chat_id is not None and user_id is not None:
            state_context = FSMContext(self.storage, chat_id=chat_id, user_id=user_id)
            kwargs["state"] = state_context

        handlers = self.get_handlers(event_type)
        for handler in handlers:
            if await handler.check(*args, **kwargs):
                async def _call(evt: Any, data: Dict[str, Any]) -> Any:
                    return await handler.call(evt, **data)

                pipeline: Callable[[Any, Dict[str, Any]], Any] = _call
                for mw in reversed(self.middlewares):
                    curr_mw = mw
                    next_call = pipeline

                    async def _wrap(evt: Any, data: Dict[str, Any], _m=curr_mw, _n=next_call) -> Any:
                        return await _m(_n, evt, data)

                    pipeline = _wrap

                return await pipeline(event, kwargs)

        return None
