from __future__ import annotations
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module="google.protobuf.*"
)

__version__ = "0.3.7"

from .client.client import Client
from .client.conversation import Conversation
from .client.manager import ClientManager
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
    SQLiteStorage,
)
from .middlewares import BaseMiddleware
from .utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
    InlineKeyboardButton,
    ReplyKeyboardButton,
)
from .utils.callback_data import CallbackData
from .utils.paginator import KeyboardPaginator
from .utils.throttler import MessageThrottler, BroadcastResult
from .utils.progress import create_progress_bar
from .filters import Command, CommandObject
from .webhook import AiohttpWebhookServer

F = MagicFilter()

__all__ = (
    "__version__",
    "Client",
    "Conversation",
    "ClientManager",
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
    "SQLiteStorage",
    "BaseMiddleware",
    "InlineKeyboardBuilder",
    "ReplyKeyboardBuilder",
    "InlineKeyboardButton",
    "ReplyKeyboardButton",
    "CallbackData",
    "KeyboardPaginator",
    "MessageThrottler",
    "BroadcastResult",
    "create_progress_bar",
    "Command",
    "CommandObject",
    "AiohttpWebhookServer",
)
