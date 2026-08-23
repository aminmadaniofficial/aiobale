from pydantic import Field
from typing import TYPE_CHECKING

from ...types import Report
from ...types.responses import DefaultResponse
from ...enums import Services
from ..base import BaleMethod


class SendReport(BaleMethod):
    """
    Sends a report for inappropriate content.

    Returns:
        aiobale.types.responses.DefaultResponse: The response indicating the success or failure of the report submission.
    """

    __service__ = Services.REPORT.value
    __method__ = "ReportInappropriateContent"

    __returning__ = DefaultResponse

    report_body: Report = Field(..., alias="1")
    """
    The body of the report containing details about the inappropriate content.
    """

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__, *, report_body: Report, **__pydantic_kwargs
        ) -> None:
            super().__init__(report_body=report_body, **__pydantic_kwargs)
