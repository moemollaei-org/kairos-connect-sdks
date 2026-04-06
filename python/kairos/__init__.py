"""Kairos SDK — Official Python client for the Kairos API."""

__version__ = "0.1.0"

from .client import Kairos, KairosSync
from .errors import (
    KairosError,
    AuthError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    InternalError,
)

__all__ = [
    "Kairos",
    "KairosSync",
    "KairosError",
    "AuthError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "InternalError",
]
