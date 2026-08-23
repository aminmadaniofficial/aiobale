from typing import Any, Optional

from .router import Router


class Dispatcher(Router):
    """
    A class that extends the functionality of the `Router` class to provide
    event dispatching capabilities. The `Dispatcher` allows for the inclusion
    of other routers and the handling of events through registered handlers.
    
    Parameters:
        name (Optional[str]): The name of the dispatcher. Defaults to "dispatcher"
        if not provided.
    """
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name or "dispatcher")

    def include_router(self, router: Router) -> None:
        for event_type, handlers in router.all_handlers().items():
            self._handlers[event_type].extend(handlers)

        for event_type in router.available_event_types():
            if event_type not in self.available_event_types():
                self.add_event_type(event_type)

    async def dispatch(self, event_type: str, *args: Any, **kwargs: Any) -> Optional[Any]:
        handlers = self.get_handlers(event_type)
        for handler in handlers:
            if await handler.check(*args, **kwargs):
                return await handler.call(*args, **kwargs)

        return None
