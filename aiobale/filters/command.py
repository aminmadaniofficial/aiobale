from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union
from .base import Filter
from ..types import Message


@dataclass
class CommandObject:
    """
    Represents parsed information about an executed command.

    Attributes:
        prefix (str): Prefix used for the command (e.g., '/', '!').
        command (str): Name of the executed command.
        args (Optional[str]): Remaining arguments passed after the command.
    """
    prefix: str
    command: str
    args: Optional[str] = None

    @property
    def args_list(self) -> List[str]:
        """Returns arguments split by whitespace as a list of strings."""
        return self.args.split() if self.args else []


class Command(Filter):
    """
    Advanced command filter for handling bot commands with custom prefixes and arguments.

    Example:
        ```python
        @dp.message(Command("start", "help", prefix="/!"))
        async def on_command(msg: Message, command: CommandObject):
            print(command.command, command.args)
        ```
    """

    def __init__(
        self,
        *commands: str,
        prefix: str = "/",
        ignore_case: bool = True,
        ignore_mention: bool = False,
    ) -> None:
        self.commands = set(c.lower() if ignore_case else c for c in commands)
        self.prefix = prefix
        self.ignore_case = ignore_case
        self.ignore_mention = ignore_mention

    def parse_command(self, text: str) -> Optional[CommandObject]:
        if not text:
            return None

        # Check if text starts with one of the allowed prefixes
        prefix_matched = None
        for p in self.prefix:
            if text.startswith(p):
                prefix_matched = p
                break

        if not prefix_matched:
            return None

        without_prefix = text[len(prefix_matched):].strip()
        if not without_prefix:
            return None

        parts = without_prefix.split(maxsplit=1)
        raw_cmd = parts[0]
        args = parts[1] if len(parts) > 1 else None

        # Handle bot mentions e.g. /start@mybot
        if "@" in raw_cmd:
            cmd_name, _ = raw_cmd.split("@", 1)
        else:
            cmd_name = raw_cmd

        check_cmd = cmd_name.lower() if self.ignore_case else cmd_name

        if self.commands and check_cmd not in self.commands:
            return None

        return CommandObject(
            prefix=prefix_matched,
            command=cmd_name,
            args=args,
        )

    async def __call__(self, event: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        text: Optional[str] = None
        if isinstance(event, Message):
            text = event.text
        elif hasattr(event, "text"):
            text = getattr(event, "text", None)
        elif isinstance(event, str):
            text = event

        if not text:
            return False

        cmd_obj = self.parse_command(text)
        if cmd_obj is None:
            return False

        # Injects command parameter into handler kwargs
        return {"command": cmd_obj}
