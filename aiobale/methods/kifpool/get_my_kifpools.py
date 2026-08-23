from ...types.responses import WalletResponse
from ...enums import Services
from ..base import BaleMethod


class GetMyKifpools(BaleMethod):
    """
    Represents the `GetMyKifpools` method of the KIFPOOL service.

    This method retrieves a list of all kifpools (wallets) owned by the authenticated user.
    """

    __service__ = Services.KIFPOOL.value
    __method__ = "GetMyKifpools"
    __returning__ = WalletResponse
