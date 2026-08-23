class AiobaleError(Exception):
    """Base exception for all Aiobale-related errors."""
    pass


class BaleError(AiobaleError):
    """
    Exception raised when an error occurs in Bale service.

    Attributes:
        message (str): A human-readable error message describing what went wrong.
        topic (int): The topic identifier where the error originated.
    """

    def __init__(self, message: str, topic: int) -> None:
        super().__init__(message)
        self.message = message
        self.topic = topic

    def __str__(self) -> str:
        return (
            f"Bale service reported an error on topic {self.topic}: {self.message}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(topic={self.topic}, message='{self.message}')"
