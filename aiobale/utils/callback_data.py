from __future__ import annotations
from typing import Any, ClassVar, Dict, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from ..filters.base import Filter
from ..utils.magic_filter import MagicFilter

T = TypeVar("T", bound="CallbackData")


class CallbackDataFilter(Filter):
    def __init__(self, callback_data_type: Type[CallbackData], magic: Optional[Any] = None) -> None:
        self.callback_data_type = callback_data_type
        self.magic = magic

    async def __call__(self, event: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        raw_data: Optional[str] = None
        if hasattr(event, "callback_data"):
            raw_data = getattr(event, "callback_data")
        elif hasattr(event, "data"):
            raw_data = getattr(event, "data")
        elif isinstance(event, str):
            raw_data = event

        if not raw_data:
            return False

        try:
            unpacked = self.callback_data_type.unpack(raw_data)
        except Exception:
            return False

        if self.magic:
            check = self.magic.resolve(unpacked)
            if not check:
                return False

        return {"callback_data": unpacked}


class CallbackData(BaseModel):
    """
    Base class for structured, type-safe callback data payloads.

    Example:
        ```python
        class ProductCB(CallbackData, prefix="product"):
            action: str
            product_id: int

        # Generate button callback
        btn_data = ProductCB(action="view", product_id=10).pack()

        # Handle button click
        @dp.message(ProductCB.filter(F.action == "view"))
        async def on_product(event, callback_data: ProductCB):
            print(callback_data.product_id)
        ```
    """
    __prefix__: ClassVar[str] = "cb"
    __separator__: ClassVar[str] = ":"

    def __init_subclass__(cls, prefix: str = "cb", sep: str = ":", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.__prefix__ = prefix
        cls.__separator__ = sep

    def pack(self) -> str:
        """Serializes callback data model into a compact string."""
        values = [self.__prefix__]
        for field_name in self.__class__.model_fields.keys():
            val = getattr(self, field_name)
            values.append(str(val))
        return self.__separator__.join(values)

    @classmethod
    def unpack(cls: Type[T], value: str) -> T:
        """Deserializes compact string back into a typed CallbackData instance."""
        parts = value.split(cls.__separator__)
        if not parts or parts[0] != cls.__prefix__:
            raise ValueError(f"Invalid prefix '{parts[0]}' for {cls.__name__}")
        field_names = list(cls.model_fields.keys())
        if len(parts) - 1 != len(field_names):
            raise ValueError(f"Expected {len(field_names)} values, got {len(parts) - 1}")
        data = {}
        for name, part in zip(field_names, parts[1:]):
            field_info = cls.model_fields[name]
            target_type = field_info.annotation
            if target_type == int:
                data[name] = int(part)
            elif target_type == float:
                data[name] = float(part)
            elif target_type == bool:
                data[name] = part.lower() in ("true", "1", "yes")
            else:
                data[name] = part
        return cls(**data)

    @classmethod
    def filter(cls: Type[T], magic_filter: Optional[Any] = None) -> CallbackDataFilter:
        """Creates a filter for matching and unpacking this CallbackData type."""
        return CallbackDataFilter(callback_data_type=cls, magic=magic_filter)
