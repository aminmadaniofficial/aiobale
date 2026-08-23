from typing import TYPE_CHECKING, Optional
from pydantic import Field, model_validator

from .service_ext import ServiceExt
from .base import BaleObject


class ServiceMessage(BaleObject):
    text: str = Field(..., alias="1")
    ext: ServiceExt = Field(..., alias="2")
