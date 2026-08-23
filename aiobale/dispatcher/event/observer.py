from typing import (
    Callable,
    Awaitable,
    Union,
    TypeVar,
    Protocol,
    Any,
    Dict,
    List,
    Optional,
)


T = TypeVar("T", bound=Callable[..., Any])


class EventDecorator(Protocol):
    def __call__(
        self, *filters: Callable[..., Union[bool, Awaitable[bool]]]
    ) -> Callable[[T], T]: ...


class EventObserver:
    """
    A class to manage event decorators and their registration.
    This class allows you to register event decorators associated with specific
    event types, retrieve the list of registered event types, and fetch the
    decorator for a specific event type.
    """
    def __init__(self) -> None:
        self._event_decorators: Dict[str, Callable[..., Any]] = {}

    def register(self, event_type: str, decorator: Callable[..., Any]) -> None:
        self._event_decorators[event_type] = decorator

    def get_registered_events(self) -> List[str]:
        return list(self._event_decorators.keys())

    def get_decorator(self, event_type: str) -> Optional[EventDecorator]:
        return self._event_decorators.get(event_type)
