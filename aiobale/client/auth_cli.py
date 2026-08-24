from __future__ import annotations

import asyncio
import time
from colorama import Fore, init
from typing import TYPE_CHECKING, Optional, Union

from ..exceptions import AiobaleError
from ..enums import SendCodeType, AuthErrors
from ..types.responses import PhoneAuthResponse
from ..utils.compat import to_thread

if TYPE_CHECKING:
    from .client import Client

init(autoreset=True)


class PhoneLoginCLI:
    """
    CLI for phone-based login using aiobale.
    Default UI language is English.
    If the user types 'fin', all subsequent messages are shown using Fingilish.
    """

    def __init__(self, client: Client):
        self.client = client
        self.fingilish_mode = False

    def _print(self, en: str, fa: str, color=Fore.WHITE):
        msg = fa if self.fingilish_mode else en
        print(color + msg)

    def _input(self, en_prompt: str, fa_prompt: str, color=Fore.WHITE) -> str:
        prompt = fa_prompt if self.fingilish_mode else en_prompt
        return input(color + prompt)

    @staticmethod
    def normalize_phone_number(raw: Union[str, int]) -> int:
        s = str(raw).strip().replace("+", "")
        if s.startswith("09"):
            s = "98" + s[1:]
        elif s.startswith("00"):
            s = s[2:]
        return int(s)

    async def start(self):
        if getattr(self.client, "phone_number", None):
            try:
                phone_number = self.normalize_phone_number(self.client.phone_number)
                self._print(
                    f"📱 Using configured phone number: {phone_number}\n",
                    f"📱 Estefadeh az shomare telefon dakhel code: {phone_number}\n",
                    Fore.CYAN,
                )
                resp = await self._send_login_request(phone_number)
                if resp:
                    success = await self._handle_code_entry(resp, phone_number)
                    if success:
                        return
            except Exception as e:
                self._print(f"⚠️ Phone error: {e}\n", f"⚠️ Khata dar shomare: {e}\n", Fore.RED)

        while True:
            phone_number = await self._request_phone_number()
            resp = await self._send_login_request(phone_number)
            if not resp:
                continue
            success = await self._handle_code_entry(resp, phone_number)
            if success:
                break

    async def _request_phone_number(self) -> int:
        self._print(
            "📱 Enter your phone number in international format:\n"
            "   Example for Iran: 98XXXXXXXXXX or 09XXXXXXXXX\n"
            "   Type 'fin' anytime to switch to Fingilish\n",
            "📱 Shomare telefon ro be format beynolmelali ya ba 09 vared kon:\n"
            "   Mesal baraye Iran: 98XXXXXXXXXX ya 09XXXXXXXXX\n"
            "   Agar mikhay zaban en beshe bezan: en\n",
            Fore.CYAN,
        )
        while True:
            raw = self._input("Phone number: ", "Shomare: ", Fore.YELLOW)
            raw = raw.replace("+", "").strip()

            low = raw.lower()
            if low == "fin":
                self.fingilish_mode = True
                self._print("✅ Fingilish mode ON.\n", "✅ Halat Fingilish fa'al shod.\n", Fore.GREEN)
                continue
            if low == "en":
                self.fingilish_mode = False
                self._print("✅ English mode ON.\n", "✅ Halat English fa'al shod.\n", Fore.GREEN)
                continue

            try:
                return self.normalize_phone_number(raw)
            except Exception:
                pass

            self._print(
                "❌ Invalid phone number format. Please check and try again.\n",
                "❌ Format shomare dorost nist. Check kon va dobare emtehan kon.\n",
                Fore.MAGENTA,
            )

    async def _send_login_request(
        self,
        phone_number: int,
        code_type: Optional[SendCodeType] = SendCodeType.DEFAULT,
    ) -> Optional[PhoneAuthResponse]:
        try:
            resp = await self.client.start_phone_auth(phone_number, code_type=code_type)
        except AiobaleError as e:
            self._print(
                f"⚠️ Aiobale error while starting phone auth: {e}\n",
                f"⚠️ Khata dar zaman ersal darkhast auth: {e}\n",
                Fore.RED,
            )
            return None
        except Exception as e:
            self._print(
                f"⚠️ Network/System error: {e}\n",
                f"⚠️ Khataye shabake/system: {e}\n",
                Fore.RED,
            )
            return None

        if isinstance(resp, AuthErrors):
            if resp == AuthErrors.PHONE_NUMBER_BANNED:
                self._print(
                    "❌ This phone number has been banned by Bale.\n",
                    "❌ In shomare tavasote bale ban shode ast.\n",
                    Fore.RED,
                )
                return None
            elif resp == AuthErrors.PHONE_NUMBER_UNREGISTERED:
                self._print(
                    "❌ This phone number is not registered in Bale. Please sign up via official app first.\n",
                    "❌ In shomare sabt nam nashode. Aval dakhele barname bale sabt nam konid.\n",
                    Fore.RED,
                )
                return None
            elif resp == AuthErrors.FLOOD:
                self._print(
                    "⚠️ Too many requests. Please wait a while before trying again.\n",
                    "⚠️ Tedade darkhast ziad bode. kami sabr konid va mojadadan talash konid.\n",
                    Fore.YELLOW,
                )
                return None
            else:
                self._print(
                    f"⚠️ Unknown auth error: {resp}\n",
                    f"⚠️ Khataye na moshakhas: {resp}\n",
                    Fore.YELLOW,
                )
                return None

        return resp

    async def _handle_code_entry(self, resp: PhoneAuthResponse, phone_number: int) -> bool:
        max_attempts = 3
        attempts = 0
        last_sent_time = time.time()
        cooldown = resp.resend_timeout.value
        expiration_timestamp = resp.code_expiration_date.value / 1000
        next_code_type = resp.next_code_type

        self._print(
            "🔑 Verification code sent! Check your SMS/Bale app.\n"
            "   Commands available during code entry:\n"
            "     - 'resend'  : request a new code (after cooldown)\n"
            "     - 'restart' : enter a different phone number\n"
            "     - 'fin'/'en': toggle language\n",
            "🔑 Code ersal shod! SMS ya barname bale ro check konid.\n"
            "   Dastoorat ghabel estefade:\n"
            "     - 'resend'  : ersale mojaddade code (pas az payane zaman)\n"
            "     - 'restart' : vared kardane yek shomare dige\n"
            "     - 'fin'/'en': taghire zaban\n",
            Fore.CYAN,
        )

        while attempts < max_attempts:
            try:
                now = time.time()
                remaining_time = expiration_timestamp - now
                elapsed = now - last_sent_time

                if remaining_time <= 0:
                    self._print(
                        "⏰ Code has expired. Restarting phone entry...\n",
                        "⏰ Mohlate code tamam shod. Bargasht be marhale shomare...\n",
                        Fore.RED,
                    )
                    return False

                self._print(
                    f"⏳ Time left before expiration: {int(remaining_time)} sec",
                    f"⏳ Zaman baghi mande ta enghaza: {int(remaining_time)} sanie",
                    Fore.YELLOW,
                )
                self._print(
                    f"⌛ New code timeout: {int(cooldown - elapsed)} sec\n",
                    f"⌛ Ta ersale dobare: {int(cooldown - elapsed)} sanie\n",
                    Fore.YELLOW,
                )

                try:
                    code = await asyncio.wait_for(
                        to_thread(
                            self._input, "Enter code: ", "Code ra vared kon: ", Fore.BLUE
                        ),
                        timeout=remaining_time,
                    )
                except asyncio.TimeoutError:
                    self._print(
                        "⏰ Code entry timed out. Please try again.\n",
                        "⏰ Mohlat vared kardan code tamoom shod. Mojadadan talash konid.\n",
                        Fore.RED,
                    )
                    return False

                code = code.strip().lower()

                if code == "fin":
                    self.fingilish_mode = True
                    self._print("✅ Fingilish mode ON.", "✅ Halat Fingilish fa'al shod.", Fore.GREEN)
                    continue
                if code == "en":
                    self.fingilish_mode = False
                    self._print("✅ English mode ON.", "✅ Halat English fa'al shod.", Fore.GREEN)
                    continue

                if code == "restart":
                    self._print(
                        "🔄 Restarting phone entry...\n",
                        "🔄 Bargasht be marhale vared kardane shomare...\n",
                        Fore.MAGENTA,
                    )
                    return False

                if code == "resend":
                    if elapsed < cooldown:
                        wait_seconds = int(cooldown - elapsed)
                        self._print(
                            f"⚠️ Wait {wait_seconds} sec before requesting a new code.\n",
                            f"⚠️ {wait_seconds} Sanie sabr kon bad dobare darkhast kon.\n",
                            Fore.RED,
                        )
                        continue

                    if next_code_type is None:
                        self._print(
                            "⚠️ Resend is not available.\n",
                            "⚠️ Emkane ersale dobare vojod nadarad.\n",
                            Fore.RED,
                        )
                        continue

                    resp = await self._send_login_request(
                        phone_number, code_type=next_code_type
                    )
                    if not resp:
                        return False

                    last_sent_time = time.time()
                    expiration_timestamp = resp.code_expiration_date.value / 1000
                    self._print("✅ Code resent!\n", "✅ Code dobare ersal shod!\n", Fore.GREEN)
                    continue

                try:
                    res = await self.client.validate_code(code, resp.transaction_hash)
                except AiobaleError as e:
                    self._print(
                        f"⚠️ Aiobale error while validating code: {e}\n",
                        f"⚠️ Khata dar zamineh-e validate kardan code: {e}\n",
                        Fore.RED,
                    )
                    return False

                if isinstance(res, AuthErrors):
                    if res == AuthErrors.WRONG_CODE:
                        self._print(
                            "❌ Incorrect code. Please try again.\n",
                            "❌ Code eshtebah ast. Tekrar kon.\n",
                            Fore.RED,
                        )
                        attempts += 1
                        if attempts >= max_attempts:
                            self._print(
                                "❌ Too many failed attempts. Restarting phone entry...\n",
                                "❌ Tedade talash ghalat ziad shod. Bargasht be shomare...\n",
                                Fore.RED,
                            )
                            return False
                    elif res == AuthErrors.PASSWORD_NEEDED:
                        return await self._handle_password_entry(resp.transaction_hash)
                    elif res == AuthErrors.SIGN_UP_NEEDED:
                        self._print(
                            "❌ First sign up using official Bale client.\n",
                            "❌ Aval dakhel khod bale sabt nam konid.\n",
                            Fore.RED,
                        )
                        return False
                    else:
                        self._print(
                            "ℹ️ An unknown authentication error occurred.\n",
                            "ℹ️ Khataye gheire moshakhas dar ehraz hoviat.\n",
                            Fore.CYAN,
                        )
                        return False

                await self._on_login_success(res)
                return True

            except Exception as e:
                self._print(
                    f"⚠️ Unexpected error: {e}\n",
                    f"⚠️ Khataye gheire montazer: {e}\n",
                    Fore.RED,
                )
                return False

    async def _handle_password_entry(self, transaction_hash: str):
        max_attempts = 3
        attempts = 0
        self._print(
            "🔐 This account requires a password.\n",
            "🔐 In hesab be password niaz darad.\n",
            Fore.MAGENTA,
        )

        while attempts < max_attempts:
            try:
                password = await asyncio.wait_for(
                    to_thread(
                        self._input, "Enter password: ", "Ramz ra vared kon: ", Fore.BLUE
                    ),
                    timeout=60,
                )
            except asyncio.TimeoutError:
                self._print(
                    "⏰ Password entry timed out. Restarting...\n",
                    "⏰ Zaman vared kardan ramz tamam shod. bargasht...\n",
                    Fore.RED,
                )
                return False

            try:
                res = await self.client.validate_password(password.strip(), transaction_hash)
            except AiobaleError as e:
                self._print(
                    f"⚠️ Aiobale error while validating password: {e}\n",
                    f"⚠️ Khata dar zamineh-e validate kardan ramz: {e}\n",
                    Fore.RED,
                )
                return False

            if isinstance(res, AuthErrors):
                if res == AuthErrors.WRONG_PASSWORD:
                    self._print(
                        "❌ Incorrect password. Try again.\n",
                        "❌ Ramz eshtebah. tekrar kon.\n",
                        Fore.RED,
                    )
                    attempts += 1
                    continue
                else:
                    self._print(
                        "ℹ️ An unknown authentication error occurred.\n",
                        "ℹ️ Khata-ye na moshakas dar ehraz hoviat.\n",
                        Fore.CYAN,
                    )
                    return False

            await self._on_login_success(res)
            return True

        self._print(
            "❌ Too many failed password attempts. Restarting...\n",
            "❌ Tedade talash barai vorood ramz ziad shod. Bargasht...\n",
            Fore.RED,
        )
        return False

    async def _on_login_success(self, res):
        self._print(
            f"🎉 Login successful! Welcome {res.user.name}",
            f"🎉 Vorood movafagh! Khosh amadid {res.user.name}",
            Fore.GREEN,
        )
