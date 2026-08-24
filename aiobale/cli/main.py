from __future__ import annotations
import sys
import os
import argparse
import pathlib
from colorama import Fore, Style, init

from .. import __version__
from ..utils.jwt_checker import parse_jwt

init(autoreset=True)

BOT_PY_TEMPLATE = """import asyncio
from aiobale import Client, Dispatcher, F
from config import BOT_TOKEN, SESSION_NAME
from handlers import common_router, admin_router
from middlewares import LoggingMiddleware

async def main():
    dp = Dispatcher()
    
    # Middlewares
    dp.middleware(LoggingMiddleware())
    
    # Routers
    dp.include_router(common_router)
    dp.include_router(admin_router)
    
    # Client initialization
    client = Client(dp, session_file=SESSION_NAME, token=BOT_TOKEN)
    
    print("🚀 Starting Bale Bot...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
"""

CONFIG_PY_TEMPLATE = """# Bot Configuration
SESSION_NAME = "my_bot.bale"
BOT_TOKEN = None  # Or paste JWT token here
ADMIN_IDS = [12345678]
"""

HANDLERS_INIT_TEMPLATE = """from .common import router as common_router
from .admin import router as admin_router

__all__ = ("common_router", "admin_router")
"""

HANDLERS_COMMON_TEMPLATE = """from aiobale import Router, F, Command, CommandObject
from aiobale.types import Message

router = Router(name="common")

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.reply("سلام! به ربات بله خوش آمدید 🚀")

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.reply("راهنمای ربات:\\n/start - شروع\\n/help - راهنما")
"""

HANDLERS_ADMIN_TEMPLATE = """from aiobale import Router, F, Command, CommandObject
from aiobale.types import Message
from config import ADMIN_IDS

router = Router(name="admin")

@router.message(Command("stats"), F.sender_id.in_(ADMIN_IDS))
async def cmd_stats(msg: Message):
    await msg.reply("📊 پنل آمار ادمین:")
"""

KEYBOARDS_INIT_TEMPLATE = """from .inline import get_main_keyboard

__all__ = ("get_main_keyboard",)
"""

KEYBOARDS_INLINE_TEMPLATE = """from aiobale.utils.keyboard import InlineKeyboardBuilder

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="وبسایت ما", url="https://aiobale.ir")
    builder.button(text="پشتیبانی", callback_data="support")
    return builder.as_markup(2)
"""

MIDDLEWARES_INIT_TEMPLATE = """from .logging import LoggingMiddleware

__all__ = ("LoggingMiddleware",)
"""

MIDDLEWARES_LOGGING_TEMPLATE = """from aiobale import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        print(f"[Event] Received: {event}")
        return await handler(event, data)
"""

REQUIREMENTS_TEMPLATE = """aiobale-py>=0.3.0
"""


def cmd_startproject(name: str) -> None:
    target_dir = pathlib.Path(name).resolve()
    if target_dir.exists():
        print(Fore.RED + f"❌ Directory '{name}' already exists!")
        return

    print(Fore.CYAN + f"📦 Generating production-ready Aiobale project in '{name}'...")

    # Create directories
    (target_dir / "handlers").mkdir(parents=True, exist_ok=True)
    (target_dir / "keyboards").mkdir(parents=True, exist_ok=True)
    (target_dir / "middlewares").mkdir(parents=True, exist_ok=True)

    # Write files
    (target_dir / "bot.py").write_text(BOT_PY_TEMPLATE, encoding="utf-8")
    (target_dir / "config.py").write_text(CONFIG_PY_TEMPLATE, encoding="utf-8")
    (target_dir / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE, encoding="utf-8")
    (target_dir / ".gitignore").write_text("*.bale\n__pycache__/\n.env\n*.db\n.venv/\n", encoding="utf-8")

    (target_dir / "handlers" / "__init__.py").write_text(HANDLERS_INIT_TEMPLATE, encoding="utf-8")
    (target_dir / "handlers" / "common.py").write_text(HANDLERS_COMMON_TEMPLATE, encoding="utf-8")
    (target_dir / "handlers" / "admin.py").write_text(HANDLERS_ADMIN_TEMPLATE, encoding="utf-8")

    (target_dir / "keyboards" / "__init__.py").write_text(KEYBOARDS_INIT_TEMPLATE, encoding="utf-8")
    (target_dir / "keyboards" / "inline.py").write_text(KEYBOARDS_INLINE_TEMPLATE, encoding="utf-8")

    (target_dir / "middlewares" / "__init__.py").write_text(MIDDLEWARES_INIT_TEMPLATE, encoding="utf-8")
    (target_dir / "middlewares" / "logging.py").write_text(MIDDLEWARES_LOGGING_TEMPLATE, encoding="utf-8")

    print(Fore.GREEN + f"✅ Project '{name}' successfully generated!")
    print(Fore.YELLOW + f"👉 Next steps:\n   cd {name}\n   pip install -r requirements.txt\n   python bot.py\n")


def cmd_session_info(file_path: str) -> None:
    p = pathlib.Path(file_path)
    if p.suffix != ".bale":
        p = p.with_suffix(".bale")

    if not p.exists():
        print(Fore.RED + f"❌ Session file '{p}' not found!")
        return

    try:
        from ..utils.grpc_post import clean_grpc
        from ..types.responses import ValidateCodeResponse
        import blackboxprotobuf

        data = p.read_bytes()
        decoded, _ = blackboxprotobuf.protobuf_to_json(clean_grpc(data))
        resp = ValidateCodeResponse.model_validate_json(decoded)

        print(Fore.GREEN + f"\n📱 Session Info: {p.name}")
        print(Fore.CYAN + f"   - User ID: {resp.user.id if resp.user else 'N/A'}")
        print(Fore.CYAN + f"   - Name: {resp.user.name if resp.user else 'N/A'}")
        print(Fore.CYAN + f"   - Username: @{resp.user.username.value if resp.user and resp.user.username else 'N/A'}")
        
        jwt_data = parse_jwt(resp.jwt.value) if resp.jwt else {}
        print(Fore.CYAN + f"   - User ID in JWT: {jwt_data.get('sub', 'N/A')}")
        print(Fore.CYAN + f"   - Issued At: {jwt_data.get('iat', 'N/A')}")
        print(Fore.CYAN + f"   - Expires At: {jwt_data.get('exp', 'N/A')}\n")
    except Exception as e:
        print(Fore.RED + f"❌ Could not parse session file: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aiobale",
        description=f"Aiobale CLI Tools (v{__version__})",
    )
    parser.add_argument("-v", "--version", action="version", version=f"Aiobale {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # startproject
    p_init = subparsers.add_parser("startproject", help="Create a new modular Aiobale bot project template")
    p_init.add_argument("name", help="Name of the project directory")

    # session info
    p_info = subparsers.add_parser("info", help="Inspect an existing .bale session file")
    p_info.add_argument("session", help="Path to the session file (e.g., my_bot.bale)")

    args = parser.parse_args()

    if args.command == "startproject":
        cmd_startproject(args.name)
    elif args.command == "info":
        cmd_session_info(args.session)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
