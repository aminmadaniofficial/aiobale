from __future__ import annotations

from pydantic import Field
from typing import TYPE_CHECKING, Optional

from ..enums import ReportKind
from .base import BaleObject
from .message_report import MessageReport
from .peer_report import PeerReport


class Report(BaleObject):
    """
    Represents a report object in Bale, describing an issue or feedback related to either a peer or a message.
    """

    kind: ReportKind = Field(..., alias="1")
    """The type/category of the report, e.g., spam, abuse, or other predefined report kinds."""

    description: Optional[str] = Field(None, alias="2")
    """Optional additional text describing the report, useful for clarifications."""

    peer_report: Optional[PeerReport] = Field(None, alias="101")
    """Detailed data related to a reported peer/user. Present only if the report targets a peer."""

    message_report: Optional[MessageReport] = Field(None, alias="102")
    """Detailed data related to a reported message. Present only if the report targets a message."""

    if TYPE_CHECKING:
        # This __init__ is only for IDE autocomplete and type checking purposes.
        # It is not executed at runtime.
        def __init__(
            __pydantic__self__,
            *,
            kind: ReportKind,
            description: Optional[str] = None,
            peer_report: Optional[PeerReport] = None,
            message_report: Optional[MessageReport] = None,
            **__pydantic_kwargs
        ) -> None:
            super().__init__(
                kind=kind,
                description=description,
                peer_report=peer_report,
                message_report=message_report,
                **__pydantic_kwargs
            )
