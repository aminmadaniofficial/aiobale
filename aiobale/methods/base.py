from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Any, Generic, TYPE_CHECKING, ClassVar

from ..client.context_controller import BotContextController


BaleType = TypeVar("BaleObject", bound=Any)


class BaleMethod(BotContextController, BaseModel, Generic[BaleType], ABC):
    """
    The abstract base class for all Bale API methods.

    Every method in the Bale platform should inherit from this class. It provides
    shared configuration, serialization rules, and service/method metadata required
    to correctly route and parse API requests and responses.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        defer_build=True,
        json_encoders={
            bool: lambda v: 1 if v else 0
        }
    )

    if TYPE_CHECKING:
        __service__: ClassVar[str]
        __method__: ClassVar[str]

        __returning__: ClassVar[Any]

    else:
        @property
        @abstractmethod
        def __service__(self) -> str:
            """
            The name of the service this method belongs to (e.g., USER, ABACUS).
            This property must be overridden by all subclasses.
            """
            pass

        @property
        @abstractmethod
        def __method__(self) -> str:
            """
            The name of the remote method as defined in the Bale API schema.
            This property must be overridden by all subclasses.
            """
            pass

        @property
        @abstractmethod
        def __returning__(self) -> type:
            """
            The expected response type returned by this method.
            This should point to a model under either aiobale.types or aiobale.types.responses.
            """
            pass
