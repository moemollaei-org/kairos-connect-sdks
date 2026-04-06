"""Error classes for the Kairos SDK."""


class KairosError(Exception):
    """Base exception for all Kairos SDK errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        request_id: str | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.request_id = request_id

    def __repr__(self) -> str:
        return (
            f"KairosError(code={self.code!r}, status_code={self.status_code}, "
            f"message={self.message!r}, request_id={self.request_id!r})"
        )


class AuthError(KairosError):
    """401 Unauthorized — authentication failed."""

    pass


class ForbiddenError(KairosError):
    """403 Forbidden — insufficient permissions."""

    pass


class NotFoundError(KairosError):
    """404 Not Found — resource does not exist."""

    pass


class ValidationError(KairosError):
    """400 Bad Request — invalid input."""

    pass


class RateLimitError(KairosError):
    """429 Too Many Requests — rate limit exceeded."""

    def __init__(
        self,
        message: str,
        retry_after: int,
        request_id: str | None = None,
    ):
        super().__init__("rate_limit_exceeded", message, 429, request_id)
        self.retry_after = retry_after

    def __repr__(self) -> str:
        return (
            f"RateLimitError(message={self.message!r}, retry_after={self.retry_after}, "
            f"request_id={self.request_id!r})"
        )


class InternalError(KairosError):
    """500 Internal Server Error — server-side error."""

    pass
