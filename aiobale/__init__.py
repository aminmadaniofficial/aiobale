from __future__ import annotations
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module="google.protobuf.*"
)

__version__ = "0.2.0"

from .client.client import Client
from .dispatcher.dispatcher import Dispatcher
from .dispatcher.router import Router
from .utils.magic_filter import MagicFilter
from .fsm import (
    State,
    StatesGroup,
    default_state,
    any_state,
    FSMContext,
    StateFilter,
    BaseStorage,
    MemoryStorage,
)
from .middlewares import BaseMiddleware
from .utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
    InlineKeyboardButton,
    ReplyKeyboardButton,
)

F = MagicFilter()

__all__ = (
    "__version__",
    "Client",
    "Dispatcher",
    "Router",
    "F",
    "State",
    "StatesGroup",
    "default_state",
    "any_state",
    "FSMContext",
    "StateFilter",
    "BaseStorage",
    "MemoryStorage",
    "BaseMiddleware",
    "InlineKeyboardBuilder",
    "ReplyKeyboardBuilder",
    "InlineKeyboardButton",
    "ReplyKeyboardButton",
)
