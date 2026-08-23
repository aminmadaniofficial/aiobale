from __future__ import annotations

from typing import Optional, Any, Dict, TYPE_CHECKING
from pydantic import ValidationInfo, model_validator

from .default import DefaultResponse
from ...types import Message, OtherMessage, ExtData

if TYPE_CHECKING:
    from ...methods import SendMessage


class MessageResponse(DefaultResponse):
    """
    Response model representing a message returned from a send message request.

    Attributes:
        message (Optional[Message]): The main message object constructed from the 
            send message method data and extended metadata.
    """

    message: Optional[Message]
    """The message created from the send request and additional extension data."""

    @model_validator(mode="before")
    @classmethod
    def add_message(cls, data: Dict[str, Any], info: ValidationInfo) -> Dict[str, Any]:
        """
        Injects a 'message' field into the data dict before model validation.

        - Checks if 'message' already exists; if so, returns data unchanged.
        - Retrieves the client from validation context, raising an error if missing.
        - Extracts the SendMessage method data from 'method_data'.
        - Parses extended data fields ('4') into ExtData objects.
        - Constructs a `previous_message` (OtherMessage) if relevant extension fields exist.
        - Handles conversion of document thumbnails (converts bytes to hex string).
        - Builds the Message instance using method data, client ID, and previous message.
        - Attaches the constructed message back into the data dictionary.
        """
        if "message" in data:
            return data

        client = info.context.get("client")
        if client is None:
            raise ValueError("client not found in context")

        method: SendMessage = data.get("method_data")
        exts = [ExtData.model_validate(value) for value in data.get("4", [])]

        # Extract previous message id and date from extensions if available
        prev_data = {
            field.name: field.value.number
            for field in exts
            if field.name in {"previous_message_rid", "previous_message_date"}
        }

        # Map extension fields to expected keys for OtherMessage
        mapped_prev_data = {}
        if "previous_message_rid" in prev_data:
            mapped_prev_data["message_id"] = prev_data["previous_message_rid"]
        if "previous_message_date" in prev_data:
            mapped_prev_data["date"] = prev_data["previous_message_date"]

        prev_message = OtherMessage.model_validate(mapped_prev_data) if mapped_prev_data else None

        # Normalize document thumbnail image bytes to hex string if present
        if hasattr(method.content, "document") and getattr(method.content.document, "thumb", None):
            thumb = method.content.document.thumb
            if isinstance(thumb.image, bytes):
                thumb.image = thumb.image.hex()

        data["message"] = Message(
            chat=method.chat,
            sender_id=client.id,
            date=data.get("2", 0),  # timestamp in milliseconds
            message_id=method.message_id,
            content=method.content,
            previous_message=prev_message,
        ).as_(client)

        return data

    if TYPE_CHECKING:
        # This init is only used for type checking and IDE autocomplete.
        # It will not be included in runtime behavior.
        def __init__(
            __pydantic__self__,
            *,
            message: Optional[Message] = None,
            **__pydantic_kwargs,
        ) -> None:
            super().__init__(message=message, **__pydantic_kwargs)
