from typing import Any
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import core_schema


class IntBool:
    """
    A custom Pydantic-compatible type to represent boolean values encoded as integers.

    In some Bale API fields, boolean values are represented as integers 0 or 1 rather than
    native booleans. This class validates and serializes such values transparently.

    All timestamp fields in the Bale API are represented as integer milliseconds since epoch.
    This class is unrelated to dates but included here for context consistency.
    """

    @classmethod
    def validate(cls, v: Any) -> bool:
        """
        Validate the input value, allowing:
          - native bool values (True/False)
          - integer 0 or 1, converted to bool

        Raises:
            ValueError: if the input is not a bool or 0/1 integer.
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, int):
            if v in (0, 1):
                return bool(v)
        raise ValueError("Must be 0 or 1 or boolean")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, handler: GetCoreSchemaHandler):
        """
        Provide Pydantic core schema with a plain validator using the `validate` method.
        """
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler):
        """
        Provide JSON schema for OpenAPI and other schema generation tools.
        Represents this type as an integer enum with values [0, 1].
        """
        json_schema = handler(schema)
        json_schema.update(type="integer", enum=[0, 1])
        return json_schema

    def __repr__(self):
        return "IntBool"

    def __str__(self):
        return "IntBool"
