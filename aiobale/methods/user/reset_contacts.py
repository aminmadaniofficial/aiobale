from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class ResetContacts(BaleMethod):
    """
    Removes all contacts from the user's contact list.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the result of the reset operation.
    """

    __service__ = Services.USER.value
    __method__ = "ResetContacts"
    
    __returning__ = DefaultResponse
