from ...types.responses import ParametersResponse
from ...enums import Services
from ..base import BaleMethod


class GetParameters(BaleMethod):
    """
    Retrieves configuration parameters from the Bale service.

    Returns:
        aiobale.types.responses.ParametersResponse: The response containing configuration parameters.
    """

    __service__ = Services.CONFIGS.value
    __method__ = "GetParameters"

    __returning__ = ParametersResponse
