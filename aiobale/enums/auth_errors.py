from enum import Enum


class AuthErrors(int, Enum):
    """
    Represents possible authentication error states.
    """

    UNKNOWN = 0
    """An unknown authentication error occurred."""

    NUMBER_BANNED = 1
    """The provided phone number is banned."""

    AUTH_LIMIT = 2
    """Too many authentication attempts; limit reached."""

    WRONG_CODE = 3
    """The verification code entered is incorrect."""

    PASSWORD_NEEDED = 4
    """A password is required to proceed with authentication."""

    SIGN_UP_NEEDED = 5
    """The account does not exist; sign-up is required."""

    WRONG_PASSWORD = 6
    """The password entered is incorrect."""

    RATE_LIMIT = 7
    """Too many requests in a short time; please wait before retrying."""

    INVALID = 8
    """The provided authentication information is invalid."""
