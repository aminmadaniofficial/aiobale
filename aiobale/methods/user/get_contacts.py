from ...types.responses import BlockedUsersResponse
from ...enums import Services
from ..base import BaleMethod


class GetContacts(BaleMethod):
    """
    Retrieves the list of contacts for the user.

    Returns:
        aiobale.types.responses.BlockedUsersResponse: The response containing the list of blocked users.
    """

    __service__ = Services.USER.value
    __method__ = "GetContacts"

    __returning__ = BlockedUsersResponse
