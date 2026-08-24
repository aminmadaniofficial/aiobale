from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict


class BaseMiddleware(ABC):
    """
    Abstract Base Middleware for processing events before and after handler execution.
    
    Example:
        class LoggingMiddleware(BaseMiddleware):
            async def __call__(
                self,
                handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
                event: Any,
                data: Dict[str, Any]
            ) -> Any:
                print(f"Before event: {event}")
                result = await handler(event, data)
                print(f"After event: {result}")
                return result
    """
    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        pass
